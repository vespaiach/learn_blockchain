from functools import reduce

from hashing import find_valid_hash, gen_hash, is_valid_hash


def get_block_transaction_str(index, transactions, pre_hash=''):
    """Get transaction string of a block.

    Arguments:
    index -- block's index.
    transactions -- list of block transaction.
    pre_hash -- previous block's hash.
    """
    tx_str = '-'.join([
        f"{tx['sender']},{tx['recipient']},{tx['amount']}" for tx in transactions])
    return f"{pre_hash}|{index}-{tx_str}"


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
nonce, hashed = find_valid_hash(
    get_block_transaction_str(0, genesis_block['transactions']))
genesis_block['hash'] = hashed
genesis_block['nonce'] = nonce

blockchain = None
block_size = 5
open_transactions = None
current_block_index = None
reward_price = 100


def init_blockchain():
    global blockchain
    global open_transactions
    global current_block_index

    blockchain = [genesis_block]
    open_transactions = [None, []]
    current_block_index = 1


def get_blockchain_values():
    """Use this function while testing to get current blockchain data"""
    return blockchain, open_transactions, current_block_index, genesis_block


def increase_block_ind_if_exceed(sender):
    """Check if current open block transactions is reaching block's size. If yes, mine a new block and clear open transactions."""
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
        'amount': reward_price
    })

    new_block = {
        'index': current_block_index,
        'transactions': open_tx
    }
    nonce, hashed = find_valid_hash(get_block_transaction_str(
        current_block_index, open_tx, blockchain[current_block_index-1]['hash']))

    new_block['hash'] = hashed
    new_block['nonce'] = nonce

    blockchain.append(new_block)


def get_balance(participant):
    """Get balance of a participant"""
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

    return reduce(lambda tx_sum, tx: tx_sum+(sum(tx) if len(tx) > 0 else 0), receive_tx, 0) + sum(open_receive_tx) - (reduce(lambda tx_sum, tx: tx_sum + (sum(tx) if len(tx) > 0 else 0), sender_tx, 0) + sum(open_sender_tx))


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
    for (index, block) in enumerate(blockchain):
        tx_str = get_block_transaction_str(
            index, block['transactions'], '' if index == 0 else blockchain[index-1]['hash'])

        hashed = gen_hash(tx_str, block['nonce'])

        if is_valid_hash(hashed) == False or hashed != block['hash']:
            return False

    return True
