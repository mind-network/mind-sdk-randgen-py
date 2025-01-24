from web3 import Web3
from eth_account import Account
from .config import config


def hot_wallet():
    web3 = Web3(Web3.HTTPProvider(config.mind_rpc_url))
    account = Account.from_key(config.hot_wallet_private_key)
    account.web3 = web3
    return account
