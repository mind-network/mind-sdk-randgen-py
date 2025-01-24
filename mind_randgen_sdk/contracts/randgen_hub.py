from web3 import Web3
from eth_utils import to_bytes
import logging
from ..config import config
from .util import load_abi
from ..hot_wallet import hot_wallet

logger = logging.getLogger(__name__)


class RandgenHub:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(config.mind_rpc_url))
        if self.web3.is_connected():
            logger.info("Connected to Mind Blockchain")
        else:
            raise ConnectionError("Failed to connect to the blockchain")
        abi = load_abi("RandgenHub.json")
        self.contract = self.web3.eth.contract(address=config.randgen_hub_address, abi=abi)

    def get_fhe_keyset_id(self):
        return self.contract.functions["fheKeySetID"]().call()

    def get_cold_wallet_address(self, hot_wallet_address=None):
        if hot_wallet_address is None:
            wallet = hot_wallet()
            hot_wallet_address = wallet.address
        return self.contract.functions["hotWalletToVoter"](hot_wallet_address).call()

    def register(self, cold_wallet_address: str = None):
        wallet = hot_wallet()
        cold_wallet_address = cold_wallet_address or config.cold_wallet_address
        registered = self.get_cold_wallet_address(hot_wallet_address=wallet.address)
        if registered == cold_wallet_address:
            raise ValueError("Voter already registered previously")
        tx = self.contract.functions.registerVoter(cold_wallet_address).build_transaction({
            'from': wallet.address,
            'nonce': wallet.web3.eth.get_transaction_count(wallet.address)
        })
        signed_tx = wallet.sign_transaction(tx)
        tx_hash = wallet.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return tx_hash

    def has_voted(self, hot_wallet_address=None):
        if hot_wallet_address is None:
            wallet = hot_wallet()
            hot_wallet_address = wallet.address
        return self.contract.functions["hasVoted"](hot_wallet_address).call()

    def is_voter_ready(self, hot_wallet_address=None):
        if hot_wallet_address is None:
            wallet = hot_wallet()
            hot_wallet_address = wallet.address
        error_code = self.contract.functions["isVoterReady"](hot_wallet_address).call()
        return error_code == 0

    def vote(self, cypher_text_url: str = None):
        if cypher_text_url is None:
            raise ValueError("cypher_text_url is missing")
        contract_payload = to_bytes(text=cypher_text_url)
        wallet = hot_wallet()
        tx = self.contract.functions.submitRandomCt(contract_payload).build_transaction({
            'from': wallet.address,
            'nonce': wallet.web3.eth.get_transaction_count(wallet.address)
        })
        tx["gas"] *= 2
        signed_tx = wallet.sign_transaction(tx)
        tx_hash = wallet.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return tx_hash
