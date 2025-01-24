from .config import config
from .contracts.randgen_hub import RandgenHub
from .contracts.fhe_key_registry import FHEKeyRegistry
from .contracts.member_pool import MemberPool
from .fhe.fhe import FHE
import time
import math
import logging

# Set up logging for the RandgenLib
logger = logging.getLogger(__name__)


class RandgenLib:
    """
    A library for managing random number generation and voting operations
    using Fully Homomorphic Encryption (FHE) and blockchain interactions.
    Implements a singleton design pattern to ensure a single instance exists.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Ensures a single instance of RandgenLib is created (Singleton pattern).
        """
        if cls._instance is None:
            cls._instance = super(RandgenLib, cls).__new__(cls)
        return cls._instance

    def __init__(self, configs=None):
        """
        Initializes the library by setting up configurations and initializing dependencies.
        Args:
            configs (dict): Optional configuration dictionary to override default settings.
        """
        if configs is not None:
            config.setup(configs)
        # Initialize contract interfaces
        self._randgen_hub = RandgenHub()
        self._fhe_key_registry = FHEKeyRegistry()
        self._member_pool = MemberPool()
        # Fetch FHE keyset and initialize FHE encryption
        keyset = self.fetch_fhe_keyset()
        self._fhe = FHE(public_key_url=keyset["public_key"]["url"])

    def register_voter(self, cold_wallet_address: str = None):
        """
        Registers a voter on the blockchain via the RandgenHub contract.
        Args:
            cold_wallet_address (str): Optional cold wallet address of the voter.
        Returns:
            Transaction hash of the registration.
        """
        return self._randgen_hub.register(cold_wallet_address=cold_wallet_address)

    def check_cold_wallet_reward(self, hub_id: int = None, cold_wallet_address: str = None):
        """
        Checks voting rewards for a specific cold wallet or hub ID.
        Args:
            hub_id (int): ID of the hub (optional).
            cold_wallet_address (str): Address of the cold wallet (optional).
        Returns:
            Reward amount for the cold wallet.
        """
        return self._member_pool.get_voting_reward(hub_id=hub_id, cold_wallet_address=cold_wallet_address)

    def fetch_fhe_keyset(self):
        """
        Fetches the FHE keyset from the key registry contract.
        Returns:
            dict: FHE keyset containing URLs and metadata.
        """
        keyset_id = self._randgen_hub.get_fhe_keyset_id()
        keyset = self._fhe_key_registry.fetch_fhe_key_set(key_id=keyset_id)
        return keyset

    def encrypt(self, num: int = None):
        """
        Encrypts a given number using FHE.
        Args:
            num (int): The number to encrypt.
        Returns:
            str: URL of the encrypted ciphertext.
        """
        return self._fhe.encrypt(num=num)

    def submit_vote(self, cypher_text_url: str = None):
        """
        Submits a vote using a ciphertext URL after verifying voter readiness and eligibility.
        Args:
            cypher_text_url (str): URL of the encrypted vote data.
        Returns:
            dict: Result of the vote submission.
        """
        is_ready = self._randgen_hub.is_voter_ready()
        if not is_ready:
            return {"status": "error", "message": "Voter is not ready"}

        # Check if the voter has already voted
        has_voted = self._randgen_hub.has_voted()
        if not has_voted[0] or time.time() > has_voted[1]:
            tx_hash = self._randgen_hub.vote(cypher_text_url=cypher_text_url)
            return {"status": "success", "tx_hash": tx_hash}
        else:
            return {
                "status": "error",
                "message": "Voter has already voted",
                "wait_seconds": math.ceil(has_voted[1] - time.time())
            }

    def vote_continuously(self):
        """
        Initiates a continuous voting process. Checks voter readiness and votes repeatedly
        at appropriate intervals based on the voting eligibility time.
        Raises:
            ValueError: If the voter is not ready.
        """
        is_ready = self._randgen_hub.is_voter_ready()
        if not is_ready:
            raise ValueError("Voter is not ready")

        while True:
            # Check if the voter has already voted
            has_voted = self._randgen_hub.has_voted()
            buffer_time = 10
            if not has_voted[0] or time.time() > (has_voted[1] + buffer_time):
                # Encrypt data and submit vote
                cypher_text_url = self._fhe.encrypt()
                tx_hash = self._randgen_hub.vote(cypher_text_url=cypher_text_url)
                logger.info({"message": "Voted successfully", "tx_hash": tx_hash})
            else:
                # Calculate sleep time and wait before the next voting round
                sleep_seconds = math.ceil(has_voted[1] - time.time()) + buffer_time
                logger.info({
                    "message": "Voter has already voted, waiting for next round",
                    "sleep_seconds": sleep_seconds
                })
                time.sleep(sleep_seconds)
