import json
import os


def load_abi(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    abi_path = os.path.join(current_dir, "abi", file_name)
    with open(abi_path, 'r') as file:
        abi = json.load(file)
    return abi
