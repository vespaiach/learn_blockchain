from datetime import datetime
import unittest

from block import Block
from chain import BlockChain, BlockChainFacade
from transaction import PendingTransaction, Transaction
from util import Hashing


class TestBlock(unittest.TestCase):
    def setUp(self):
        self.created_at = datetime.now()
        self.block = Block(index=1, transactions=[
            Transaction('Tom', 'Jerry', 100),
            Transaction('Tony', 'Jerry', 100),
            Transaction('Jerry', 'Max', 100),
        ], created_at=self.created_at)

        return super().setUp()

    def test_build_block_st(self):
        self.assertEqual(str(
            self.block), f"{1}{self.created_at.strftime('%m/%d/%y,%H:%M:%S')}{''.join(list(map(lambda tx: str(tx),self.block.transactions)))}")

    def test_is_valid(self):
        self.block.find_hash('pre_hash')

        self.assertTrue(self.block.is_valid('pre_hash'))
        self.assertTrue(self.block.nonce >= 0)
        self.assertTrue(Hashing.is_valid_hash(self.block.hash))

    def test_get_balance(self):
        self.assertEqual(self.block.get_balance('Tom'), -100)
        self.assertEqual(self.block.get_balance('Tony'), -100)
        self.assertEqual(self.block.get_balance('Jerry'), 100)
        self.assertEqual(self.block.get_balance('Max'), 100)


class TestTransaction(unittest.TestCase):
    def test_transaction_str(self):
        tx = Transaction('Tom', 'Jerry', 1001)

        self.assertEqual(str(tx), "TomJerry1001")

    def test_get_balance(self):
        tx = Transaction('Tom', 'Jerry', 1001)

        self.assertEqual(tx.get_balance('Tom'), -1001)
        self.assertEqual(tx.get_balance('Jerry'), 1001)
        self.assertEqual(tx.get_balance('Random'), 0)


class TestPendingTransaction(unittest.TestCase):
    def setUp(self):
        self.pending_tx = PendingTransaction()

    def test_add(self):
        self.pending_tx.add(Transaction('Tom', 'Jerry', 100))

        self.assertEqual(len(self.pending_tx), 1)

    def test_get_balance(self):
        self.pending_tx.add(Transaction('Tom', 'Jerry', 100))
        self.pending_tx.add(Transaction('Tom', 'Max', 100))

        self.assertEqual(self.pending_tx.get_balance('Tom'), -200)
        self.assertEqual(self.pending_tx.get_balance('Jerry'), 100)
        self.assertEqual(self.pending_tx.get_balance('Max'), 100)
        self.assertEqual(self.pending_tx.get_balance('Other'), 0)

    def test_read(self):
        self.pending_tx.add(Transaction('Tom', 'Jerry', 100))
        self.pending_tx.add(Transaction('Tom', 'Max', 100))

        self.assertEqual(len(self.pending_tx.read()), 2)
        self.assertEqual(len(self.pending_tx), 0)


class TestBlockChain(unittest.TestCase):
    def setUp(self) -> None:
        self.chain = BlockChainFacade()
        self.chain.add_genesis_transactions([
            Transaction('GENESIS', 'Tom', 1000),
            Transaction('GENESIS', 'Tony', 1000),
            Transaction('GENESIS', 'Max', 1000),
        ])

    def test_add_tx(self):
        self.chain.add_transaction(Transaction('Tom', 'Jerry', 500))
        self.chain.add_transaction(Transaction('Tom', 'Tony', 500))
        self.chain.add_transaction(Transaction('Max', 'Tom', 100))
        self.chain.add_transaction(Transaction('Max', 'Tony', 100))
        self.chain.add_transaction(Transaction('Max', 'Joe', 200))

        self.assertTrue(self.chain.verify_chain())
        self.assertEqual(self.chain.get_balance('Tom'), 100)
        self.assertEqual(self.chain.get_balance('Tony'), 1600)
        self.assertEqual(self.chain.get_balance('Jerry'), 500)
        self.assertEqual(self.chain.get_balance('Max'), 700)
        self.assertEqual(self.chain.get_balance('Joe'), 200)
        self.assertEqual(self.chain.get_balance('Henry'), 0)


class TestHashing(unittest.TestCase):
    def test_is_valid_hash(self):
        self.assertFalse(Hashing.is_valid_hash('sdflkasiowekrjlsdfilsdf'))
        self.assertFalse(Hashing.is_valid_hash('00234sdflkasiowekrjlsdfilsdf'))
        self.assertFalse(Hashing.is_valid_hash('s'*64))

    def test_find_valid_hash(self):
        hashed, nonce = Hashing.find_valid_hash('',
                                                '1-Tom,Teo,200-Tom,Ti,200-Tony,Max,200-Tony-Henry,200-Tony,Mary,200-REWARD,Tony,100')

        self.assertTrue(nonce >= 0)
        self.assertTrue(len(hashed) == 64)
        self.assertTrue(hashed[0:2] == '00')


if __name__ == '__main__':
    unittest.main()
