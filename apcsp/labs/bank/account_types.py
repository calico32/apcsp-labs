from hashlib import pbkdf2_hmac
from secrets import token_bytes
from typing import List, Optional

from .account import Account, BalanceAccount

OVERDRAFT_FEE = 25_00


def _desc(msg: str, desc: str | None = None) -> str:
    return f"{msg} - {desc}" if desc else msg


class CheckingAccount(BalanceAccount):
    def __init__(
        self,
        owner: "UserAccount",
        name: Optional[str] = None,
        overdraft_source: Optional[BalanceAccount] = None,
    ) -> None:
        super().__init__("checking", name or "Checking Account")
        owner._accounts.append(self)
        self._owner = owner
        self._balance = 0
        self._overdraft_source = overdraft_source

    @property
    def overdraft_source(self) -> Optional[BalanceAccount]:
        return self._overdraft_source

    def withdraw(self, amount: int, description: str | None = None) -> None:
        if self._balance < 0:
            raise ValueError("Currently overdrawn; cannot withdraw")
        if amount < 0:
            raise ValueError("Cannot withdraw negative amount")

        if amount > self._balance:
            if self._overdraft_source is not None:
                self._overdraft_source.withdraw(
                    amount - self._balance,
                    _desc(f"Overdraft from {self.name}", description),
                )
                self._post(-self.balance, _desc("Overdraft partial", description))
                self._post(
                    -OVERDRAFT_FEE,
                    _desc(
                        f"Fee for overdraft from {self._overdraft_source.name}",
                        description,
                    ),
                )
                self._balance -= self.balance + OVERDRAFT_FEE
            else:
                raise ValueError("Insufficient funds")
        else:
            self._balance -= amount
            self._post(-amount, description or "Withdrawal")


class SavingsAccount(BalanceAccount):
    def __init__(self, owner: "UserAccount", name: Optional[str] = None) -> None:
        super().__init__("savings", name or "Savings Account")  # type: ignore
        owner._accounts.append(self)
        self._owner = owner
        self._balance = 0

    def add_interest(self, interest: int) -> int:
        """
        Adds interest to the savings account
        interest: the interest rate to add, in thousandths of a percent
        Returns: the amount of interest added, in cents
        """
        amount = (self._balance * interest) // 1000_000
        self._balance += amount
        self._post(amount, f"Interest of {interest // 1000_0}.{interest % 1000_0:02d}%")
        return amount


PBKDF2_ROUNDS = 100_000

UserHoldableAccount = CheckingAccount | SavingsAccount


def pbkdf2(password: str, salt: bytes) -> bytes:
    return pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ROUNDS)


class UserAccount(Account):
    _accounts: List[UserHoldableAccount]

    def __init__(self, name: str, username: str, password: str, pin: str) -> None:
        super().__init__("user", name)
        self._accounts = []
        self._username = username
        self._salt = token_bytes(32)
        self._password = pbkdf2(password, self._salt)
        self._pin = pbkdf2(pin, self._salt)

    @property
    def username(self) -> str:
        return self._username

    @property
    def type(self) -> str:
        return "user"

    @property
    def accounts(self) -> List[UserHoldableAccount]:
        return self._accounts

    def login(self, password: str) -> bool:
        return self._password == pbkdf2(password, self._salt)

    def set_password(self, password: str) -> None:
        self._password = pbkdf2(password, self._salt)

    def set_pin(self, pin: str) -> None:
        self._pin = pbkdf2(pin, self._salt)

    def check_pin(self, pin: str) -> bool:
        return self._pin == pbkdf2(pin, self._salt)

    def close_account(self, account: UserHoldableAccount) -> None:
        self._accounts.remove(account)

    def str(self, indent: int = 0) -> str:
        header = f"{' ' * indent}User Account: {self.name} ({self.id})"
        if len(self._accounts) == 0:
            return f"{header}\n{' ' * (indent + 4)}No accounts"

        account_str = "\n".join(acc.account_str(indent + 4) for acc in self._accounts)
        return f"{header}\n{account_str}"
