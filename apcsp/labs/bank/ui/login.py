from typing import Any

from ..bank import BankState
from .prompt import _error, press_any_key, prompt_str
from .util import clear, title


def login(bank: BankState) -> Any:
    clear()
    title("Login")

    username = prompt_str("Username: ")
    password = prompt_str("Password: ", hide=True)

    acc = bank.login(username, password)
    if not acc:
        _error("Invalid username or password.")
        press_any_key()
        return None

    return True


def logout(bank: BankState) -> Any:
    bank.logout()
    return True
