import list_all_balances
import transfer
import get_all_transactions_data

menu_options = {
    1: 'List all balances',
    2: 'Send funds to investors',
    3: 'Download all transactions data',
    0: 'Exit',
}


def print_menu():
    print("--------------\nUnofficial SOL helper\n--------------")
    print("What you'd like to do today?\n--------------")
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


def option1():
    list_all_balances.get_list_of_all_balances()


def option2(mode, threshold=10):
    transfer.send_funds_to_investors(mode=mode, threshold=threshold)


def option3():
    get_all_transactions_data.get_all_transactions_data()


if __name__ == '__main__':
    while True:
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')

        # Check what choice was entered and act accordingly
        if option == 1:
            print("OK. Let's do it!")
            option1()

        elif option == 2:
            mode_transfer = str(input('Which mode do you prefer? Enter all/not all: ')).lower()
            if mode_transfer != "all":
                threshold_sol = int(input('Enter SOL threshold (this amount will remain in the wallet): '))
                option2(mode_transfer, threshold_sol)
                print("OK. Let's do it!")
            else:
                option2(mode_transfer)

        elif option == 3:
            print("OK. Let's do it!")
            option3()

        elif option == 0:
            print('Bye!')
            exit()

        else:
            print('Invalid option. Please enter a number between 1 and 2')
