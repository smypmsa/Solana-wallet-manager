import csv
import time

from solana.publickey import PublicKey
from solana.rpc.api import Client

from utils import get_transaction_data as utils


def get_all_transactions_data():
    client = Client("https://api.mainnet-beta.solana.com")

    # Get all addresses to check
    with open('files/addresses.csv') as f:
        reader = csv.reader(f)
        wallets = list(reader)

    # Process each wallet address in the list
    for wallet in wallets:
        wallet_data = []
        print(wallet[0])
        public_address = PublicKey(wallet[0])
        signatures = client.get_confirmed_signature_for_address2(public_address)

        # Process each signature (tx) made with this wallet address
        for signature in signatures['result']:
            tx_data = []
            time.sleep(1)

            for attempt in range(3):
                try:
                    tx = client.get_confirmed_transaction(signature['signature'])
                    tx_data = utils.get_transaction_data(tx, signature=signature['signature'], wallet=wallet[0])
                    wallet_data.extend(tx_data)
                    print(f"Completed {signature['signature']}")
                except Exception as err:
                    print(f"Error occurred {signature['signature']}: {err.args}")
                    time.sleep(1)
                    # Try another attempt
                    continue
                # If no exception let's break attempt loop
                break

            # Check if all attempts have been used and transaction data is empty
            if attempt == 2 and not tx_data:
                wallet_data.append([f"Error occurred while processing transaction: {signature[signature]}."])

        # Save wallet transactions and balance changes to the file
        with open('files/transactions.csv', 'a') as f:
            write = csv.writer(f)
            write.writerows(wallet_data)
            time.sleep(1)
