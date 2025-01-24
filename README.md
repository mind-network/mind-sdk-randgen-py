# **Mind Network Randgen Hub Voter CLI & SDK**

A Python-based Command Line Interface (CLI) and SDK to interact with the **Randgen Hub** on the **Mind Network**. This tool provides functionalities such as voter registration, reward checking, encryption, and anonymous voting powered by Fully Homomorphic Encryption (FHE). The hub is live and accessible at [Randgen Hub](https://dapp.mindnetwork.xyz/votetoearn/voteonhubs/3).

---

## **Features**
- **Voter Registration**: Register your hot wallet as a voter in the Randgen Hub.
- **Reward Checking**: Check voting rewards associated with your hot and cold wallets.
- **Anonymous Voting**: Perform one-time or continuous voting in eligible rounds, with anonymity guaranteed by FHE.
- **Fully Homomorphic Encryption (FHE)**: Leverage FHE for secure and privacy-preserving voting.
- **Encryption**: Encrypt data using the FHE key set.
- **Vote Submission**: Submit encrypted votes to the Randgen Hub.
- **SDK for Programmatic Usage**: Use the SDK to integrate functionalities into your own projects.

---

## **Installation**

### **Prerequisites**
- **Python** (version 3.10 or later)
- **pip** (Python Package Installer)

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

---

## **CLI Usage**

The CLI provides various commands for interacting with the Randgen Hub. Below is a list of available commands:

### **register-voter**
Registers the hot wallet as a voter in the Randgen Hub.
```bash
python -m randgen_cli register-voter [--hot-wallet-private-key <key>] [--cold-wallet-address <address>]
```

### **check-voting-reward**
Checks the voting rewards for the hot and cold wallets.
```bash
python -m randgen_cli check-voting-reward [--hot-wallet-private-key <key>] [--cold-wallet-address <address>]
```

### **print-fhe-keyset**
Fetches and displays the Fully Homomorphic Encryption (FHE) key set.
```bash
python -m randgen_cli print-fhe-keyset
```

### **encrypt**
Encrypts a given number using FHE.
```bash
python -m randgen_cli encrypt <number>
```

### **submit-vote**
Submits a vote using an encrypted ciphertext URL.
```bash
python -m randgen_cli submit-vote <ciphertextUrl> [--hot-wallet-private-key <key>]
```

### **vote-once**
Performs a single voting action in the Randgen Hub.
```bash
python -m randgen_cli vote-once [--hot-wallet-private-key <key>]
```

### **vote-nonstop**
Continuously votes in every eligible round in the Randgen Hub.
```bash
python -m randgen_cli vote-nonstop [--hot-wallet-private-key <key>]
```

---

## **Using as an SDK**

You will be able to integrate the project programmatically into your Python projects using the SDK. The SDK will expose a range of business functions, such as:
- `register_voter`: Register a voter in the Randgen Hub.
- `check_hot_wallet_reward`: Check rewards associated with the hot wallet.
- `check_cold_wallet_reward`: Check rewards associated with the cold wallet.
- `fetch_fhe_keyset`: Fetch the FHE key set for encryption operations.
- `encrypt`: Encrypt a number using the FHE key set.
- `submit_vote`: Submit a vote using an encrypted ciphertext.
- `vote_once`: Perform a one-time vote in the Randgen Hub.
- `vote_continuously`: Continuously vote in all eligible rounds in the Randgen Hub.

---

## **License**

This project is licensed under the **MIT License**.

---

## **Contact**

For questions or support, please contact [Mind Network Official Channels](https://mindnetwork.xyz/).