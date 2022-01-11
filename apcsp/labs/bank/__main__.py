import os

from .account_types import CheckingAccount, SavingsAccount, UserAccount

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

print(alice.str())
print(bob.str())
print(charlie.str())

# Output:
"""
User Account: Alice (u0)
    Primary Savings (savings, s0): $1,000.00
        +$1,000.00 - Deposit
    Checking Account (checking, c0): $501,523.23
        +$1,523.23 - Paycheck
        +$500,000.00 - Transfer from Savings Account (s1) owned by Bob (u1)
User Account: Bob (u1)
    Savings Account (savings, s1): $505,499.52
        +$1,000.00 - Deposit
        +$1,000,000.00 - Deposit
        -$765.44 - Overdraft from Checking Account - New PC
        -$500,000.00 - Transfer to Checking Account (c0) owned by Alice (u0)
        +$5,264.96 - Interest of 1.525%
    Checking Account (checking, c1): -$25.00
        +$1,234.56 - Paycheck
        -$1,234.56 - Overdraft partial - New PC
        -$25.00 - Fee for overdraft from Savings Account - New PC
User Account: Charlie (u2)
    No accounts
"""
