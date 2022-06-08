import csv
from config import bcolors, LAMPORTS_PER_SOL
from datetime import datetime
from solana.rpc.api import Client


def get_list_of_all_balances():

    total = 0
    client = Client("https://api.mainnet-beta.solana.com")

    with open('files/addresses.csv') as f:
        reader = csv.reader(f)
        wallets = list(reader)

    data = []
    for w in wallets:
        balance = round(client.get_balance(w[0])['result']['value'] / LAMPORTS_PER_SOL, 2)
        data.append([w[0], balance])
        total += balance
        if balance > 10:
            print(f"{bcolors.OKGREEN}{w[0]} = {balance}{bcolors.ENDC}")
        else:
            print(f"{w[0]} = {balance}")

    print(f'{datetime.now().strftime("%m%d_%H%M%S")} - Total SOL: {total}')

    with open(f'files/balances_{datetime.now().strftime("%m%d_%H%M%S")}.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows(data)
