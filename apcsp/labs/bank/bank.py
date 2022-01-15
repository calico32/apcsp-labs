from typing import Dict

from .account_types import (
    CheckingAccount,
    SavingsAccount,
    UserAccount,
    UserHoldableAccount,
)


class Bank(object):
    accounts: Dict[str, UserAccount] = {}

    def __init__(self):
        self.accounts = {}

    def login(self, username: str, password: str) -> UserAccount | None:
        if username in self.accounts:
            account = self.accounts[username]
            if account.login(password):
                return account

        return None

    def register(
        self, name: str, username: str, password: str, pin: str
    ) -> UserAccount:
        if username in self.accounts:
            raise RuntimeError("Username already taken")

        account = UserAccount(name, username, password, pin)
        self.accounts[username] = account
        return account


class BankState(object):
    user: UserAccount | None

    def __init__(self, bank: Bank) -> None:
        self.bank = bank
        self.user = None

    def login(self, username: str, password: str) -> UserAccount | None:
        acc = self.bank.login(username, password)
        if acc:
            self.user = acc
        return acc

    def logout(self) -> None:
        self.user = None

    def username_taken(self, username: str) -> bool:
        return username in self.bank.accounts

    def delete_user_account(self) -> None:
        if self.user is None:
            raise RuntimeError("Must be logged in to delete an account.")

        self.bank.accounts.pop(self.user.username)
        self.user = None

    def register(
        self, name: str, username: str, password: str, pin: str
    ) -> UserAccount:
        acc = self.bank.register(name, username, password, pin)
        self.user = acc
        return acc

    def open_account(
        self,
        account_type: str,
        name: str | None,
        overdraft_source: UserHoldableAccount | None = None,
    ) -> UserHoldableAccount:
        if self.user is None:
            raise RuntimeError("Must be logged in to open an account.")

        acc: UserHoldableAccount
        if account_type == "checking":
            acc = CheckingAccount(self.user, name or None, overdraft_source)
        elif account_type == "savings":
            acc = SavingsAccount(self.user, name or None)
        else:
            raise RuntimeError("Invalid account type.")

        return acc

    def close_account(self, account_id: str) -> None:
        if self.user is None:
            raise RuntimeError("Must be logged in to close an account.")

        acc = self.get_account(account_id)
        if not acc:
            raise RuntimeError("Invalid account ID.")

        self.user.close_account(acc)

    def find_account(self, account_id: str) -> UserHoldableAccount | None:
        acc = self.get_account(account_id)

        if not acc:
            all_accounts = [
                acc
                for acclist in self.bank.accounts.values()
                for acc in acclist.accounts
            ]
            matches = list(filter(lambda a: a.id == account_id, all_accounts))
            if not matches:
                return None
            assert len(matches) == 1, "Multiple accounts with same ID"
            return matches[0]

        return acc

    def get_account(self, account_id: str) -> UserHoldableAccount | None:
        if self.user is None:
            raise RuntimeError("Must be logged in to access an account.")

        acc = list(filter(lambda a: a.id == account_id, self.user.accounts))
        if not acc:
            return None
        assert len(acc) == 1, "Multiple accounts with same ID"
        return acc[0]
