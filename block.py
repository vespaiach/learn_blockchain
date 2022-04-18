from datetime import datetime
from util import Balance, Hashing


class Block(Balance):
    def __init__(self, index, transactions, nonce=None, hash=None, created_at=datetime.now()):
        self.index = index
        self.created_at = created_at
        self.nonce = nonce
        self.transactions = transactions

        self.hash = hash
        self.__tx_str = None

    def __str__(self):
        self.__tx_str = ''.join(
            [str(tx) for tx in self.transactions]) if self.__tx_str is None else self.__tx_str

        return f"{self.index}{self.created_at.strftime('%m/%d/%y,%H:%M:%S')}{self.__tx_str}"

    def find_hash(self, pre_hash):
        self.hash, self.nonce = Hashing.find_valid_hash(pre_hash, str(self))

    def is_valid(self, pre_hash):
        if Hashing.is_valid_hash(self.hash) == False:
            return False

        hashed = Hashing.generate_hash(
            f"{pre_hash}{str(self)}{str(self.nonce)}")

        if hashed != self.hash or Hashing.is_valid_hash(hashed) == False:
            return False

        return True

    def get_balance(self, participant: str) -> int:
        return sum([tx.get_balance(participant) for tx in self.transactions])
