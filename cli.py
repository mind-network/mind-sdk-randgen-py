import typer
import json
import os
import logging
from mind_randgen_sdk.randgen_lib import RandgenLib

# Configure logging for the CLI tool
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the path for the configuration file
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, "mind_randgen_sdk", "configs", "config.json")

# Load configuration from the JSON file
config = {}
if os.path.exists(config_path):
    with open(config_path, "r") as file:
        config = json.load(file)
        logging.info("Config file loaded")


# Create a Typer app instance
app = typer.Typer()


# CLI command to register a voter
@app.command()
def register_voter(hot_wallet_private_key: str = None, cold_wallet_address: str = None):
    """
    Register a voter using a hot wallet private key and a cold wallet address.
    Args:
        hot_wallet_private_key (str): Private key for the hot wallet.
        cold_wallet_address (str): Address of the cold wallet.
    """
    try:
        if hot_wallet_private_key is not None:
            config["hot_wallet_private_key"] = hot_wallet_private_key
        lib = RandgenLib(configs=config)
        tx_hash = lib.register_voter(cold_wallet_address)
        logging.info({"message": "Registration successful", "tx_hash": tx_hash})
    except Exception as e:
        logging.error({"error": e})


# CLI command to check voting rewards
@app.command()
def check_voting_reward(cold_wallet_address: str = None):
    """
    Check the voting reward for a given cold wallet address.
    Args:
        cold_wallet_address (str): Address of the cold wallet.
    """
    try:
        lib = RandgenLib(configs=config)
        reward_amount = lib.check_cold_wallet_reward(cold_wallet_address=cold_wallet_address)
        logging.info({"reward_amount": reward_amount})
    except Exception as e:
        logging.error({"error": e})


# CLI command to print the Fully Homomorphic Encryption (FHE) keyset
@app.command()
def print_fhe_keyset():
    """
    Fetch and print the FHE keyset from the library.
    """
    try:
        lib = RandgenLib(configs=config)
        keyset = lib.fetch_fhe_keyset()
        logging.info({"keyset": keyset})
    except Exception as e:
        logging.error({"error": e})


# CLI command to encrypt a number
@app.command()
def encrypt(num: int):
    """
    Encrypt a given number using the library's encryption functionality.
    Args:
        num (int): Number to be encrypted.
    """
    try:
        lib = RandgenLib(configs=config)
        logging.info({"encrypting": num})
        cypher_text_url = lib.encrypt(num=num)
        logging.info({"cypher_text_url": cypher_text_url})
    except Exception as e:
        logging.error({"error": e})


# CLI command to submit a vote
@app.command()
def submit_vote(cypher_text_url: str, hot_wallet_private_key: str = None):
    """
    Submit a vote using a cypher text URL and optionally a hot wallet private key.
    Args:
        cypher_text_url (str): URL of the encrypted vote data.
        hot_wallet_private_key (str): Private key for the hot wallet (optional).
    """
    try:
        if hot_wallet_private_key is not None:
            config["hot_wallet_private_key"] = hot_wallet_private_key
        lib = RandgenLib(configs=config)
        result = lib.submit_vote(cypher_text_url=cypher_text_url)
        logging.info(result)
    except Exception as e:
        logging.error({"error": e})


# CLI command to vote continuously
@app.command()
def vote_nonstop(hot_wallet_private_key: str = None):
    """
    Start a continuous voting process using the hot wallet private key.
    Args:
        hot_wallet_private_key (str): Private key for the hot wallet (optional).
    """
    try:
        if hot_wallet_private_key is not None:
            config["hot_wallet_private_key"] = hot_wallet_private_key
        lib = RandgenLib(configs=config)
        lib.vote_continuously()
    except Exception as e:
        logging.error({"error": e})


# Entry point for the CLI tool
if __name__ == "__main__":
    app()
