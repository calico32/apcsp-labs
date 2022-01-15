from .account_types import CheckingAccount, SavingsAccount, UserAccount
from .bank import Bank
from .ui import ui_main

bank = Bank()

alice = bank.register("Alice", "alice", "aaaaaaaa", "1234")
bob = bank.register("Bob", "bob", "bbbbbbbb", "1234")
charlie = bank.register("Charlie", "charlie", "cccccccc", "1234")

bob_checking = CheckingAccount(bob, "Bob's Checking")
bob_checking.deposit(1000_00, "Initial deposit")

charlie_checking = CheckingAccount(charlie, "Charlie's Checking")
charlie_savings = SavingsAccount(charlie, "Charlie's Savings")
charlie_savings.deposit(1000000_00, "Initial deposit")

"""
Test accounts (username:password:pin):
alice:aaaaaaaa:1234 - test user (u0) with no accounts
bob:bbbbbbbb:1234 - test user (u1) with one checking account (c0)
charlie:cccccccc:1234 - test user (u2) with one checking (c1) and one savings account (s0)

Feel free to create your own accounts.
"""

ui_main(bank)
