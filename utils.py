from prettytable import PrettyTable


def print_blockchain(blockchain):
    draw_arrow = False

    for block in blockchain:
        if draw_arrow == True:
            print('  |')
            print('  |')
            print('  |')
            print('  |')
            print('  V')

        print('Index:       {:<64}'.format(block['index']))
        print('Nonce:       {:<64}'.format(block['nonce']))
        print('Hash:        {:<64}'.format(block['hash']))
        print('\nTransactions:')

        tb = PrettyTable()
        tb.field_names = ["Order", "Sender", "Recipiant", "Amount"]

        for (i, tx) in enumerate(block['transactions']):
            tb.add_row([i, tx['sender'], tx['recipient'], tx['amount']])

        print(tb)

        draw_arrow = True
