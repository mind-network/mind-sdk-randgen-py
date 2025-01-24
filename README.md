
# **Mind Network Randgen Hub Voter CLI & SDK**

A Python-based **Command Line Interface (CLI)** and **Software Development Kit (SDK)** for interacting with the **Randgen Hub** on the **Mind Network**. This tool facilitates voter registration, reward checking, encryption, and secure anonymous voting using **Fully Homomorphic Encryption (FHE)**.

The hub is live and accessible at [Randgen Hub](https://dapp.mindnetwork.xyz/votetoearn/voteonhubs/3).

---

## **Features**

- **Voter Registration**: Register for voting in the Randgen Hub.
- **Reward Checking**: Retrieve rewards linked to your wallet after voting.
- **Anonymous Voting**: Cast encrypted votes in a secure and privacy-preserving manner using FHE.
- **Encryption**: Encrypt data with the FHE keyset.
- **Vote Submission**: Submit encrypted votes to the Randgen Hub.
- **Continuous Voting**: Automatically vote in eligible rounds using the `vote_nonstop` functionality.
- **Python SDK for Integration**: Use the SDK to integrate these features into your Python projects.

---

## **Installation**

### **Prerequisites**
- **Python 3.10+**

### **Steps**

1. Clone the repository:
   ```bash
   git clone https://github.com/mind-network/mind-sdk-randgen-py.git
   ```

2. Navigate to the project directory:
   ```bash
   cd mind-sdk-randgen-py
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy default configuration and modify as needed:
   ```bash
   cp mind_randgen_sdk/configs/default_config.json mind_randgen_sdk/configs/config.json
   ```

5. Run the CLI:
   ```bash
   python cli.py --help
   ```

---

## **CLI Usage**

The CLI provides commands to interact with the Randgen Hub. Below is a list of available commands:

### **register-voter**
Registers a voter in the Randgen Hub.
```bash
python cli.py register-voter [--hot-wallet-private-key <key>] [--cold-wallet-address <address>]
```
- **Options**:
  - `--hot-wallet-private-key` (optional): Private key of the hot wallet.
  - `--cold-wallet-address` (optional): Address of the cold wallet for receiving rewards.

### **check-voting-reward**
Checks voting rewards for a specific wallet.
```bash
python cli.py check-voting-reward [--cold-wallet-address <address>]
```
- **Options**:
  - `--cold-wallet-address` (optional): Address of the cold wallet.

### **print-fhe-keyset**
Displays the Fully Homomorphic Encryption (FHE) keyset.
```bash
python cli.py print-fhe-keyset
```

### **encrypt**
Encrypts a number using FHE.
```bash
python cli.py encrypt <number>
```
- **Arguments**:
  - `<number>`: The number to encrypt.

### **submit-vote**
Submits a vote using an encrypted ciphertext URL.
```bash
python cli.py submit-vote <ciphertextUrl> [--hot-wallet-private-key <key>]
```
- **Arguments**:
  - `<ciphertextUrl>`: URL of the encrypted vote.
  - `--hot-wallet-private-key` (optional): Private key of the hot wallet.

### **vote-nonstop**
Continuously votes in every eligible round of the Randgen Hub.
```bash
python cli.py vote-nonstop [--hot-wallet-private-key <key>]
```
- **Options**:
  - `--hot-wallet-private-key` (optional): Private key of the hot wallet.

---

## **Using as an SDK**

You can integrate this project into your Python applications programmatically by importing the `RandgenLib` class.

### **Installation**
Install the SDK using `pip`:
```bash
pip install mind_randgen_sdk
```

### **Available Methods**

The following methods are provided by the SDK:
- `register_voter(cold_wallet_address: str)`: Register a voter in the Randgen Hub.
- `check_cold_wallet_reward(cold_wallet_address: str)`: Check rewards associated with a cold wallet.
- `fetch_fhe_keyset()`: Retrieve the FHE keyset.
- `encrypt(num: int)`: Encrypt a number using the FHE keyset.
- `submit_vote(cypher_text_url: str)`: Submit an encrypted vote.
- `vote_continuously()`: Continuously vote in all eligible rounds.

### **Code Example**
Below is an example of generating a random number, encrypting it, and submitting a vote:
```python
from mind_randgen_sdk import RandgenLib

# Initialize the library
configs = {
    "hot_wallet_private_key": "your_private_key",
    "other_config_values": "..."
}
lib = RandgenLib(configs=configs)

# Generate a random number
random_number = 42
print(f"Generated random number: {random_number}")

# Encrypt the random number
encrypted_url = lib.encrypt(num=random_number)
print(f"Encrypted URL: {encrypted_url}")

# Submit the vote
result = lib.submit_vote(cypher_text_url=encrypted_url)
print("Vote submission result:", result)
```

---

## **Configuration**

The CLI uses a configuration file located at `configs/config.json` if the file is present. For reference on the required settings, you can check the default configuration file at `configs/default_config.json`.

---

## **License**

This project is licensed under the **MIT License**.

---

## **Contact**

For questions or support, please contact [Mind Network Official Channels](https://mindnetwork.xyz/).
