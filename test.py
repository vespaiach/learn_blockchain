import unittest

from blockchain import get_block_values, init_blockchain, add_transaction, get_balance, verify_blockchain


class TestBlock(unittest.TestCase):
    def setUp(self):
        init_blockchain()
        return super().setUp()

    def test_initial_block(self):
        """Test the initial block function"""
        blockchain, open_transactions, current_block_index, genesis_block = get_block_values()
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


class TestTransaction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_blockchain()
        return super().setUpClass()

    def test_add_transaction_success(self):
        """Test add_transaction success"""
        result = add_transaction(sender='Tony', recipient='Jemy', amount=100)
        blockchain, open_transactions, current_block_index, genesis_block = get_block_values()

        open_tx = open_transactions[current_block_index]

        self.assertEqual(current_block_index, 1)
        self.assertTrue(result)
        self.assertTrue(len([tx for tx in open_tx if tx['sender'] ==
                        'Tony' and tx['recipient'] == 'Jemy' and tx['amount'] == 100]) > 0)

    def test_add_transaction_fail(self):
        """Test add_transaction fail because of exceeding balance"""
        result = add_transaction(
            sender='Tony', recipient='Max', amount=1001)
        blockchain, open_transactions, current_block_index, genesis_block = get_block_values()

        open_tx = open_transactions[current_block_index]

        self.assertFalse(result)
        self.assertEqual(current_block_index, 1)
        self.assertEqual(len([tx for tx in open_tx if tx['sender'] ==
                              'Tony' and tx['recipient'] == 'Max' and tx['amount'] == 1001]), 0)

    def test_add_transaction_fail(self):
        """Test add_transaction fail because of zero balance"""
        result = add_transaction(
            sender='Guest', recipient='Max', amount=1000)
        blockchain, open_transactions, current_block_index, genesis_block = get_block_values()

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
        return super().setUpClass()

    def text_balance(self):
        self.assertEqual(get_balance('Tony'), 500)
        self.assertEqual(get_balance('Tom'), 600)

    def text_block(self):
        blockchain, open_transactions, current_block_index, genesis_block = get_block_values()

        self.assertEqual(current_block_index, 2)
        self.assertEqual(open_transactions, [None, None, []])
        self.assertEqual(
            blockchain[1]['hash'], '1-Tom,Teo,200-Tom,Ti,200-Tony,Max,200-Tony-Henry,200-Tony,Mary,200-REWARD,Tony,100')


class TestVerifyBlockchain(unittest.TestCase):
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

    def text_verify_blockchain(self):
        self.assertTrue(verify_blockchain())


if __name__ == '__main__':
    unittest.main()
