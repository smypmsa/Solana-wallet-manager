import csv
from datetime import datetime

from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer

from config import bcolors, TRANSFER_R_I, LAMPORTS_PER_SOL, FEE


def send_funds_to_investors(mode="not all", threshold=10):

    client = Client("https://api.mainnet-beta.solana.com")
    logs = []
    report = []

    folder_id_runners = "ids_runners/"
    folder_id_investors = "ids_source/"

    for investor in TRANSFER_R_I:
        # For each investor in the list, get seed bytes and public address
        with open(f"{folder_id_investors}{investor[0]}.json") as file:
            seed = file.read()
        seed_array = [int(i) for i in seed[1:-1].split(',')]
        # Convert seed string to bytes
        seed_bytes = bytes(seed_array)
        investor_keypair = Keypair.from_secret_key(seed_bytes)
        # Reset total amount sent for each investor
        total_amount_sent = 0

        # For each runner linked to the investor, get seed bytes and keypair from which SOL must be transferred
        for runner in investor[1]:
            with open(f"{folder_id_runners}{runner}.json") as file:
                seed = file.read()
            seed_array = [int(i) for i in seed[1:-1].split(',')]
            # Convert seed string to bytes
            seed_bytes = bytes(seed_array)
            sender_keypair = Keypair.from_secret_key(seed_bytes)

            balance_lamports = client.get_balance(sender_keypair.public_key)['result']['value']

            if mode == 'all':
                # Withdraw ALL funds from runners' wallets
                amount_to_send_lamports = balance_lamports - FEE * LAMPORTS_PER_SOL
                if amount_to_send_lamports < 0.01 * LAMPORTS_PER_SOL:
                    # Skip this runner's wallet if SOL balance is less than 0.01 SOL
                    print(f"Balance is too low {round(amount_to_send_lamports / LAMPORTS_PER_SOL, 2)} "
                          f"({sender_keypair.public_key})")
                    logs.append([f"{sender_keypair.public_key} not processed: too low balance "
                                 f"({round(amount_to_send_lamports / LAMPORTS_PER_SOL, 2)} SOL)"])
                    continue
            else:
                # Partial withdraw
                if balance_lamports > threshold * LAMPORTS_PER_SOL:
                    # Leave some SOL on balance
                    amount_to_send_lamports = balance_lamports - (threshold * LAMPORTS_PER_SOL) - (FEE * LAMPORTS_PER_SOL)

                    if amount_to_send_lamports < (0.1 * LAMPORTS_PER_SOL):
                        print(f"{bcolors.WARNING}Balance is too low {round(balance_lamports / LAMPORTS_PER_SOL, 2)} "
                              f"({sender_keypair.public_key}){bcolors.ENDC}")
                        continue

                else:
                    # Next wallet
                    print(f"{bcolors.WARNING}Balance is too low {round(balance_lamports / LAMPORTS_PER_SOL, 2)} "
                          f"({sender_keypair.public_key}){bcolors.ENDC}")
                    logs.append([f"{sender_keypair.public_key} not processed: too low balance "
                                 f"({round(balance_lamports / LAMPORTS_PER_SOL, 2)} SOL)"])
                    continue

            print(f"Ready to send {round(amount_to_send_lamports / LAMPORTS_PER_SOL, 2)} "
                  f"from {sender_keypair.public_key} to {investor_keypair.public_key}")

            tx = Transaction().add(transfer(TransferParams(from_pubkey=sender_keypair.public_key,
                                                           to_pubkey=investor_keypair.public_key,
                                                           lamports=int(amount_to_send_lamports))))

            tx_signature = client.send_transaction(tx, sender_keypair)
            # Check that transaction has been FINALIZED
            for attempt in range(5):
                try:
                    tx_response = client.confirm_transaction(tx_signature['result'])
                    logs.append([f"RUNNER: {sender_keypair.public_key} - {runner} - {investor[0]} - "
                                 f"{round(amount_to_send_lamports / LAMPORTS_PER_SOL, 2)} SOL"])
                    print(f"{bcolors.OKGREEN}Success{bcolors.ENDC}"
                          "-------")

                    total_amount_sent += round(amount_to_send_lamports / LAMPORTS_PER_SOL, 2)

                except Exception as err:
                    logs.append([f"{sender_keypair.public_key} not processed: "
                                 f"{err.args}"])
                    print(f"{bcolors.WARNING}Fail{bcolors.ENDC}"
                          "-------")
                    continue
                break

        # Save total amount sent to an investor
        report.append([investor[0], total_amount_sent])

    print("FINISH")

    with open(f'files/logs_{datetime.now().strftime("%m%d_%H%M%S")}.csv', 'a') as f:
        write = csv.writer(f)
        write.writerows(logs)

    # Save total amount sent to an investor
    with open(f'reports/report_{datetime.now().strftime("%m%d_%H%M%S")}.csv', 'a') as f:
        write = csv.writer(f)
        write.writerows(report)
