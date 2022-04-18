from functools import reduce
from util import Balance, TransactionBorg


class Transaction(Balance):
    def __init__(self, sender: str, recipient: str, amount: int) -> None:
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def __str__(self):
        return f"{self.sender}{self.recipient}{str(self.amount)}"

    def get_balance(self, participant: str) -> int:
        if self.sender == participant:
            return -self.amount
        elif self.recipient == participant:
            return self.amount
        else:
            return 0


class PendingTransaction(TransactionBorg, Balance):
    def __init__(self):
        self.__transactions = []

    def __len__(self):
        return len(self.__transactions)

    def add(self, tx: Transaction) -> None:
        self.__transactions.append(tx)

    def read(self):
        """Return pending transactions and reset transaction list"""
        tx = self.__transactions[:]
        self.__transactions = []
        return tx

    def get_balance(self, participant: str) -> int:
        return sum([tx.get_balance(participant) for tx in self.__transactions])
