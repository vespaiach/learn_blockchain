from typing import List
from block import Block
from transaction import PendingTransaction, Transaction
from util import Balance, print_blockchain


class BlockChain(Balance):
    def gen_genesis_block(self, transactions: List[Transaction]) -> None:
        tx = transactions[:]

        block = Block(index=0, transactions=tx)
        block.find_hash('')

        self.__chain.append(block)

    def __init__(self, reward_price=100):
        self.__chain = []
        self.reward_price = reward_price

    def mine_block(self, transactions: List[Transaction], miner: str) -> None:
        tx = transactions[:]
        tx.append(Transaction('REWARD', miner, self.reward_price))

        block = Block(index=len(self.__chain), transactions=tx)
        pre_block = self.__chain[-1]

        block.find_hash(pre_block.hash)

        self.__chain.append(block)

    def get_balance(self, participant: str) -> int:
        return sum([block.get_balance(participant) for block in self.__chain])

    def verify_chain(self) -> bool:
        for (index, block) in enumerate(self.__chain):
            if block.is_valid('' if index == 0 else self.__chain[index-1].hash) == False:
                return False

        return True

    def print_chain(self) -> None:
        print_blockchain(self.__chain)


class BlockChainFacade:

    def __init__(self, block_size=5, reward_price=100) -> None:
        self.__chain = BlockChain(reward_price)
        self.__pending_tx = PendingTransaction()
        self.__block_size = block_size

    def get_balance(self, participant: str) -> int:
        return self.__chain.get_balance(participant) + self.__pending_tx.get_balance(participant)

    def __mine_block_if_exceed_size(self, miner) -> None:
        if len(self.__pending_tx) == self.__block_size:
            self.__chain.mine_block(self.__pending_tx.read(), miner)

    def add_genesis_transactions(self, txs: List[Transaction]) -> None:
        self.__chain.gen_genesis_block(txs)

    def add_transaction(self, tx: Transaction) -> bool:
        if self.get_balance(tx.sender) < tx.amount:
            return False

        self.__pending_tx.add(tx)

        self.__mine_block_if_exceed_size(tx.sender)

    def verify_chain(self):
        return self.__chain.verify_chain()

    def print_blockchain(self) -> None:
        self.__chain.print_chain()
