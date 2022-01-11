import os
from typing import List

from .account import Account
from .account_types import CheckingAccount, SavingsAccount, UserAccount
from .bank_ui import ui_main

os.system("clear")


class Bank:
    _accounts: List[Account]
    _users: List[UserAccount]

    def __init__(self):
        self._accounts = []
        self._users = []


bank = Bank()

alice = UserAccount("Alice")
alice_savings = SavingsAccount(alice, "Primary Savings")
alice_checking = CheckingAccount(alice, overdraft_source=alice_savings)

bob = UserAccount("Bob")
bob_savings = SavingsAccount(bob)
bob_checking = CheckingAccount(bob, overdraft_source=bob_savings)

charlie = UserAccount("Charlie")

alice_savings.deposit(1000_00)
bob_savings.deposit(1000_00)
bob_savings.deposit(1000000_00)

alice_checking.deposit(1523_23, "Paycheck")
bob_checking.deposit(1234_56, "Paycheck")

bob_checking.withdraw(2000_00, "New PC")

bob_savings.transfer(alice_checking, 500000_00)

bob_savings.add_interest(1_0525)

ui_main(bank)
