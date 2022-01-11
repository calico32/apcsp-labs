from typing import List, Literal, Tuple

from .util import create_id, format_amount


def format_name(acc: "Account", in_relation_to: "Account | None" = None) -> str:
    if in_relation_to is None:
        return f"{acc.name} ({acc.id})"

    if (
        hasattr(acc, "_owner")
        and hasattr(in_relation_to, "_owner")
        and acc._owner != in_relation_to._owner  # type: ignore
    ):
        return f"{acc.name} ({acc.id}) owned by {acc._owner.name} ({acc._owner.id})"  # type: ignore

    return f"{acc.name} ({acc.id})"


def transfer_msg(
    source: "BalanceAccount",
    dest: "BalanceAccount",
) -> Tuple[str, str]:
    source_name = format_name(source, dest)
    dest_name = format_name(dest, source)

    return (f"Transfer to {dest_name}", f"Transfer from {source_name}")


class Transaction:
    def __init__(self, amount: int, description: str) -> None:
        self.amount = amount
        self.description = description

    def str(self, indent=0) -> str:
        return f"{' ' * indent}{format_amount(self.amount)} - {self.description}"


class Account:
    _id: str
    _type: str
    _name: str

    def __init__(self, type: str, name: str) -> None:
        assert len(type) > 0, "Account type cannot be empty"
        assert len(name) > 0, "Account name cannot be empty"
        self._type = type
        self._name = name
        self._id = create_id(type[0])

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        assert len(name) > 0, "Account name cannot be empty"
        self._name = name

    @property
    def type(self):
        return self._type


class BalanceAccount(Account):
    _balance: int
    _transactions: List[Transaction]
    _owner: "Account"

    def __init__(self, type: str, name: str) -> None:
        super().__init__(type, name)
        self._balance = 0
        self._transactions = []
        pass

    @property
    def balance(self) -> int:
        return self._balance

    @property
    def balance_str(self) -> str:
        return format_amount(self._balance, include_sign="negative")

    @property
    def transactions(self) -> List[Transaction]:
        return self._transactions

    def transactions_str(self, indent: int = 0) -> str:
        if len(self._transactions) == 0:
            return ""

        return "\n".join(t.str(indent) for t in self._transactions)

    def account_str(self, indent: int = 0) -> str:
        header = (
            f"{' ' * indent}{self.name} ({self.type}, {self.id}): {self.balance_str}"
        )
        if len(self._transactions) > 0:
            return header + "\n" + self.transactions_str(indent + 4)
        else:
            return header

    def _post(self, amount: int, description: str) -> None:
        self._transactions.append(Transaction(amount, description))

    def deposit(self, amount: int, description: str | None = None) -> None:
        if amount < 0:
            raise ValueError("Cannot deposit negative amount")

        self._balance += amount
        self._post(amount, description or "Deposit")

    def withdraw(self, amount: int, description: str | None = None) -> None:
        if amount < 0:
            raise ValueError("Cannot withdraw negative amount")

        if amount > self._balance:
            raise ValueError("Insufficient funds")

        self._balance -= amount
        self._post(-amount, description or "Withdrawal")

    def transfer(self, other: "BalanceAccount", amount: int) -> None:
        if self is other:
            raise ValueError("Cannot transfer to self")

        if amount < 0:
            raise ValueError("Cannot transfer negative amount")

        to_msg, from_msg = transfer_msg(self, other)

        try:
            self.withdraw(amount, to_msg)
        except ValueError as e:
            raise ValueError(to_msg) from e

        # deposit cannot fail because we already checked for negative amount
        other.deposit(amount, from_msg)
