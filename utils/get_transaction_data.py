from datetime import datetime
from config import LAMPORTS_PER_SOL


def get_transaction_data(tx, signature: str, wallet: str):
    """
    Take tx object, return balance changes.
    :param wallet: wallet address
    :param tx: transaction object
    :param signature: transaction signature
    :return: list of balance changes, including SOL changes
    """

    tx_datetime = datetime.fromtimestamp(tx['result']['blockTime'])

    pre_balance = tx['result']['meta']['preTokenBalances']
    post_balance = tx['result']['meta']['postTokenBalances']
    pre_sol_balance = tx['result']['meta']['preBalances']
    post_sol_balance = tx['result']['meta']['postBalances']
    data = []

    # GET ALL SPL CHANGES
    for balance in pre_balance:
        wallet_address = balance['owner']
        transaction_amount = balance['uiTokenAmount']['uiAmountString']
        transaction_token = balance['mint']
        data.append([wallet, 'pre_balance', str(tx_datetime), signature,
                     wallet_address, transaction_amount, transaction_token])

    for balance in post_balance:
        wallet_address = balance['owner']
        transaction_amount = balance['uiTokenAmount']['uiAmountString']
        transaction_token = balance['mint']
        data.append([wallet, 'post_balance', str(tx_datetime), signature,
                     wallet_address, transaction_amount, transaction_token])

    i = 0
    transaction_token = 'SOL'

    # GET ALL SOL CHANGES
    while i <= len(pre_sol_balance) - 2:
        wallet_address_pre = tx['result']['transaction']['message']['accountKeys'][i]
        transaction_amount_pre = pre_sol_balance[i] / LAMPORTS_PER_SOL

        wallet_address_post = tx['result']['transaction']['message']['accountKeys'][i]
        transaction_amount_post = post_sol_balance[i] / LAMPORTS_PER_SOL

        # Add record only if amounts are different
        if transaction_amount_pre != transaction_amount_post:
            data.append([wallet, 'pre_sol_balance', str(tx_datetime), signature,
                         wallet_address_pre, transaction_amount_pre, transaction_token])

            data.append([wallet, 'post_sol_balance', str(tx_datetime), signature,
                         wallet_address_post, transaction_amount_post, transaction_token])
        # Next
        i += 1

    return data
