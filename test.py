import unittest

from blockchain import get_blockchain_values, init_blockchain, add_transaction, get_balance, verify_blockchain
from hashing import find_valid_hash, is_valid_hash
from utils import print_blockchain


class TestBlock(unittest.TestCase):
    def setUp(self):
        init_blockchain()
        return super().setUp()

    def test_initial_block(self):
        """Test the initial block function"""
        blockchain, open_transactions, current_block_index, genesis_block = get_blockchain_values()
        self.assertEqual(blockchain, [genesis_block])
        self.assertEqual(open_transactions, [None, []])
        self.assertEqual(current_block_index, 1)


class TestBalance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_blockchain()
        add_transaction('Tom', 'Teo', 200)
        add_transaction('Tom', 'Ti', 200)
        return super().setUpClass()

    def text_balance(self):
        self.assertEqual(get_balance('Tom'), 600)
        self.assertEqual(get_balance('Teo'), 200)
        self.assertEqual(get_balance('Ti'), 200)


class TestAddTransaction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_blockchain()
        return super().setUpClass()

    def test_add_transaction_success(self):
        result = add_transaction(sender='Tony', recipient='Jemy', amount=100)
        blockchain, open_transactions, current_block_index, genesis_block = get_blockchain_values()

        open_tx = open_transactions[current_block_index]

        self.assertEqual(current_block_index, 1)
        self.assertTrue(result)
        self.assertTrue(len([tx for tx in open_tx if tx['sender'] ==
                        'Tony' and tx['recipient'] == 'Jemy' and tx['amount'] == 100]) > 0)

    def test_add_transaction_fail(self):
        result = add_transaction(
            sender='Tony', recipient='Max', amount=1001)
        blockchain, open_transactions, current_block_index, genesis_block = get_blockchain_values()

        open_tx = open_transactions[current_block_index]

        self.assertFalse(result)
        self.assertEqual(current_block_index, 1)
        self.assertEqual(len([tx for tx in open_tx if tx['sender'] ==
                              'Tony' and tx['recipient'] == 'Max' and tx['amount'] == 1001]), 0)

    def test_add_transaction_fail(self):
        """Test add_transaction fail because of zero balance"""
        result = add_transaction(
            sender='Guest', recipient='Max', amount=1000)
        blockchain, open_transactions, current_block_index, genesis_block = get_blockchain_values()

        open_tx = open_transactions[current_block_index]

        self.assertFalse(result)
        self.assertEqual(current_block_index, 1)
        self.assertEqual(len([tx for tx in open_tx if tx['sender'] ==
                              'Guest' and tx['recipient'] == 'Max' and tx['amount'] == 1000]), 0)


class TestMineBlock(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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

        return super().setUpClass()

    def test_balance(self):
        self.assertEqual(get_balance('Tom'), 600)
        self.assertEqual(get_balance('Tony'), 690)
        self.assertEqual(get_balance('Teo'), 430)
        self.assertEqual(get_balance('Ti'), 250)
        self.assertEqual(get_balance('Max'), 1200)
        self.assertEqual(get_balance('Mary'), 1020)
        self.assertEqual(get_balance('Henry'), 200)
        self.assertEqual(get_balance('Jerry'), 810)

    def test_mine_a_new_block(self):
        blockchain, open_transactions, current_block_index, genesis_block = get_blockchain_values()

        print_blockchain(blockchain)

        self.assertEqual(current_block_index, 3)
        self.assertEqual(open_transactions, [None, None, None, []])
        self.assertEqual(len(blockchain), 3)
        self.assertTrue(verify_blockchain())


class TestHashing(unittest.TestCase):
    def test_is_valid_hash(self):
        self.assertFalse(is_valid_hash('sdflkasiowekrjlsdfilsdf'))
        self.assertFalse(is_valid_hash('00234sdflkasiowekrjlsdfilsdf'))
        self.assertFalse(is_valid_hash('s'*64))

    def test_find_valid_hash(self):
        nonce, hashed = find_valid_hash(
            '1-Tom,Teo,200-Tom,Ti,200-Tony,Max,200-Tony-Henry,200-Tony,Mary,200-REWARD,Tony,100')

        self.assertTrue(nonce >= 0)
        self.assertTrue(len(hashed) == 64)
        self.assertTrue(hashed[0:2] == '00')


if __name__ == '__main__':
    unittest.main()
