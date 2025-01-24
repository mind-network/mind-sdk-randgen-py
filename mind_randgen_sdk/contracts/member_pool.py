from web3 import Web3
import logging
from ..config import config
from .util import load_abi

logger = logging.getLogger(__name__)


class MemberPool:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(config.mind_rpc_url))
        if self.web3.is_connected():
            logger.info("Connected to Mind Blockchain")
        else:
            raise ConnectionError("Failed to connect to the blockchain")
        abi = load_abi("MemberPool.json")
        self.contract = self.web3.eth.contract(address=config.member_pool_address, abi=abi)

    def get_voting_reward(self, hub_id: int = None, cold_wallet_address: str = None):
        cold_wallet_address = cold_wallet_address or config.cold_wallet_address
        hub_id = hub_id or config.hub_id
        return self.contract.functions["voterRewardEarned"](cold_wallet_address, hub_id).call()
