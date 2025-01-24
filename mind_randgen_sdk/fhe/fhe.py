import requests
import logging
from web3 import Web3
from ..config import config
from ..hot_wallet import hot_wallet
from .fhe_client import FHEClient

logger = logging.getLogger(__name__)


class FHE:
    def __init__(self, public_key_url: str = None):
        if public_key_url is None:
            raise ValueError("public_key_url is missing")
        result = requests.get(public_key_url)
        result.raise_for_status()
        self.fhe = FHEClient(public_key=result.text)
        logger.info({"msg": "FHE initialized", "public_key_url": public_key_url})

    def encrypt(self, num: int = None) -> str:
        if num is None:
            encrypted = self.fhe.get_random_u8()
            logger.debug("Random number generated")
            if encrypted:
                return self.save_fcn_input(encrypted)
            else:
                logger.error("Unable to generate random number")
                raise RuntimeError("Random number generation failed")
        else:
            encrypted = self.fhe.encrypt_u8(num)
            if encrypted:
                return self.save_fcn_input(encrypted)
            else:
                logger.error(f"Unable to encrypt number {num}")
                raise RuntimeError("Number encryption failed")

    def save_fcn_input(self, base64_encoded: str) -> str:
        wallet = hot_wallet()
        hash_value = Web3.keccak(base64_encoded.encode('utf-8'))
        signature = wallet.unsafe_sign_hash(hash_value)
        payload = {
            "subnet_id": config.hub_id,
            "wallet": wallet.address,
            "signature": Web3.to_hex(signature.signature),
            "fhe_content": base64_encoded
        }
        response = requests.post(config.public_storage_url, json=payload)
        response.raise_for_status()
        cypher_text_url = response.json()["url"]
        return cypher_text_url
