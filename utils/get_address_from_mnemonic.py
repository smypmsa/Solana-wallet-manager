import csv
from bip_utils import *
from config import PROJECT_PATH

"""
Read the list of seeds (index, seed).
Generate address and save address to the new list (index, address).
Save seed as a separate json-file.
"""


with open(f'{PROJECT_PATH}files/seeds.csv') as f:
    reader = csv.reader(f)
    seeds = list(reader)

for seed in seeds:
    try:
        seed_bytes = Bip39SeedGenerator(seed[1], lang=Bip39Languages.ENGLISH).Generate("")
        bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA)
        bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
        bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)

        with open(f'{PROJECT_PATH}files/new_addresses.csv', 'w') as f:
            print(bip44_chg_ctx.PublicKey().ToAddress())
            writer = csv.writer(f)
            writer.writerow([seed[0], bip44_chg_ctx.PublicKey().ToAddress()])

        with open(f'{PROJECT_PATH}ids_to_process/{seed[0]}.json', 'w') as f:
            writer = csv.writer(f)
            writer.writerow([seed[1]])

    except Exception as err:
        with open(f'{PROJECT_PATH}files/new_addresses.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([f"error {err.args}"])
