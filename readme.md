# Solana wallets manager
### Description
This repo contains CLI app for managing Solana wallets. In particular, it will be useful for monitoring balances, transferring SOL, scanning transactions.

### How to install and run the script
Install Python 3.8+.
Run "pip3 install -r requirements.txt".

1. Update config.py file.
2. Run main.py.
3. Follow the instruction in the console.

### Directories
#### files
Save here the list of addresses (csv). The directory is for logs, balances, transactions data.
#### ids_runners
Json-files containing keypairs of wallets which it is required to monitor and check.
#### ids_source
Json-files containing keypairs of wallets which is for storing SOL from 'runners' wallets.
#### reports
Reports on transferred SOL tokens from 'runners' wallets.
#### utils
Python modules called in the main.py, and a useful function for receiving SOL address from seed phrases of such wallets as Phantom.

### DISCLAIMER
The project is at draft stage. That means all code only for educational purposes. Please do not use it in the production environment.