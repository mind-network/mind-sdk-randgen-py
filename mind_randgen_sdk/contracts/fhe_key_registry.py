from web3 import Web3
import logging
from ..config import config
from .util import load_abi

logger = logging.getLogger(__name__)


class FHEKeyRegistry:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(config.mind_rpc_url))
        if self.web3.is_connected():
            logger.info("Connected to Mind Blockchain")
        else:
            raise ConnectionError("Failed to connect to the blockchain")
        abi = load_abi("FheKeyRegistry.json")
        self.contract = self.web3.eth.contract(address=config.fhe_key_registry_address, abi=abi)

    def fetch_fhe_key_set(self, key_id: int):
        keyset = self.contract.functions["fheKeySets"](key_id).call()
        keys = ["private_key", "compute_key", "public_key"]
        result = {}
        for key, entry in zip(keys, keyset):
            url, key_hash, signature, signer = entry
            result[key] = {
                "url": url,
                "key_hash": key_hash,
                "signature": signature,  # Decode binary signature for readability
                "signer": signer
            }
        return result
