from abc import abstractmethod
from hashlib import sha256
from typing import Dict, Tuple
from prettytable import PrettyTable


class TransactionBorg:
    __share_state: Dict[str, str] = {}

    def __init__(self) -> None:
        self.__dict__ = self.__share_state


class Balance:
    @abstractmethod
    def get_balance(self, participant: str) -> int:
        pass


class Hashing:
    @staticmethod
    def is_valid_hash(hash: str) -> bool:
        return len(hash) == 64 and hash[0:2] == '00'

    @staticmethod
    def generate_hash(st: str) -> str:
        return sha256(st.encode()).hexdigest()

    @staticmethod
    def find_valid_hash(pre_hash: str, st: str) -> Tuple[str, int]:
        nonce = 0
        hashing = Hashing.generate_hash(f"{pre_hash}{st}{str(nonce)}")

        while Hashing.is_valid_hash(hashing) == False:
            nonce += 1
            hashing = Hashing.generate_hash(f"{pre_hash}{st}{str(nonce)}")

        return hashing, nonce


def print_blockchain(blockchain):
    draw_arrow = False

    for block in blockchain:
        if draw_arrow == True:
            print('|')
            print('|')
            print('|')
            print('V')

        print('Index      :{}'.format(block.index))
        print('Nonce      :{}'.format(block.nonce))
        print('Hash       :{}'.format(block.hash))
        print('Created At :{}'.format(block.created_at))
        print('\nTransactions:')

        tb = PrettyTable()
        tb.field_names = ["Order", "Sender", "Recipiant", "Amount"]

        for (i, tx) in enumerate(block.transactions):
            tb.add_row([i, tx.sender, tx.recipient, tx.amount])

        print(tb)

        draw_arrow = True
