from prettytable import PrettyTable


def get_block_hash(block, previous_hash):
    tx_hash = '-'.join(
        f"{tx['sender']},{tx['recipient']},{tx['amount']}" for tx in block['transactions'])
    return f"{previous_hash}|{block['index']}-{tx_hash}"


genesis_block = {
    'index': 0,
    'transactions': [
        {'sender': 'GENESIS', 'recipient': 'Max', 'amount': 1000},
        {'sender': 'GENESIS', 'recipient': 'Mary', 'amount': 1000},
        {'sender': 'GENESIS', 'recipient': 'Jerry', 'amount': 1000},
        {'sender': 'GENESIS', 'recipient': 'Tom', 'amount': 1000},
        {'sender': 'GENESIS', 'recipient': 'Tony', 'amount': 1000},
    ],
}
genesis_block['hash'] = get_block_hash(genesis_block, '')
blockchain = None
block_size = 5
open_transactions = None
current_block_index = None


def init_blockchain():
    global blockchain
    global open_transactions
    global current_block_index

    blockchain = [genesis_block]
    open_transactions = [None, []]
    current_block_index = 1


def get_block_values():
    return blockchain, open_transactions, current_block_index, genesis_block


def increase_block_ind_if_exceed(sender):
    global current_block_index
    global open_transactions

    open_tx = open_transactions[current_block_index]

    if (len(open_tx) == block_size):
        mine_block(sender)

        open_transactions[current_block_index] = None
        current_block_index += 1
        open_transactions.append([])


def mine_block(miner):
    global current_block_index

    open_tx = open_transactions[current_block_index][:]
    open_tx.append({
        'sender': 'REWARD',
        'recipient': miner,
        'amount': 100
    })
    new_block = {
        'index': current_block_index,
        'transactions': open_tx
    }
    new_block['hash'] = get_block_hash(
        new_block, blockchain[current_block_index-1]['hash'])

    blockchain.append(new_block)


def get_balance(participant):
    global open_transactions
    global current_block_index

    open_tx = open_transactions[current_block_index]

    sender_tx = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant]
                 for block in blockchain]
    open_sender_tx = [tx['amount']
                      for tx in open_tx if tx['sender'] == participant]

    receive_tx = [[tx['amount'] for tx in block['transactions']
                   if tx['recipient'] == participant] for block in blockchain]
    open_receive_tx = [tx['amount']
                       for tx in open_tx if tx['recipient'] == participant]

    return sum([amount[0] if len(amount) > 0 else 0 for amount in receive_tx]) + sum(open_receive_tx) - (sum([amount[0] if len(amount) > 0 else 0 for amount in sender_tx]) + sum(open_sender_tx))


def is_valid_tx(sender, amount):
    return get_balance(sender) >= amount


def add_transaction(sender, recipient, amount):
    if is_valid_tx(sender, amount):
        open_transactions[current_block_index].append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        increase_block_ind_if_exceed(sender)
        return True

    return False


def verify_blockchain():
    for (block, index) in enumerate(blockchain):
        if index == 0:
            continue
        if get_block_hash(block, blockchain[index-1].hash) != block.hash:
            return False

    return True


def print_blockchain():
    draw_arrow = False

    for block in blockchain:
        if draw_arrow == True:
            print('  |')
            print('  |')
            print('  |')
            print('  |')
            print('  V')

        print('Index', block['index'])
        print('Hash', block['hash'])

        tb = PrettyTable()
        tb.field_names = ["Order", "Sender", "Recipiant", "Amount"]

        for (i, tx) in enumerate(block['transactions']):
            tb.add_row([i, tx['sender'], tx['recipient'], tx['amount']])

        print(tb)

        draw_arrow = True


init_blockchain()
add_transaction('Tom', 'Teo', 200)
add_transaction('Tom', 'Ti', 200)
add_transaction('Tony', 'Max', 200)
add_transaction('Tony', 'Henry', 200)
add_transaction('Tony', 'Mary', 200)

add_transaction('Mary', 'Teo', 200)
add_transaction('Teo', 'Ti', 50)
add_transaction('Tony', 'Jerry', 10)
add_transaction('Jerry', 'Tony', 200)
add_transaction('Teo', 'Mary', 20)
print_blockchain()
