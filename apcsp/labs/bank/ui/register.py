from string import ascii_letters, digits
from typing import Any

from colorama import Fore, Style  # type: ignore

from ..bank import Bank, BankState
from .prompt import _error, press_any_key, prompt_str
from .util import clear, print_accounts, title

USERNAME_CHARS = ascii_letters + digits + "_"


def validate_name(name: str) -> bool:
    if len(name) < 2:
        _error("Name must be at least 2 characters.")
        return False
    return True


def validate_username(username: str) -> bool:
    if len(username) < 3:
        _error("Username must be at least 3 characters in length.")
        return False
    if len(username) >= 20:
        _error("Username must be at most 20 characters length.")
        return False

    for c in username:
        if c not in USERNAME_CHARS:
            _error(
                "Username must consist of only alphanumeric characters and underscores."
            )
            return False

    return True


def validate_pin(pin: str) -> bool:
    if len(pin) != 4 or not pin.isdigit():
        _error("PIN must be 4 digits.")
        return False
    return True


def validate_password(password: str) -> bool:
    if len(password) < 8:
        _error("Password must be at least 8 characters.")
        return False
    return True


def register(state: BankState) -> Any:
    if state.user:
        _error("Already logged in. Please log out first.")
        return True

    clear()
    title("Register")

    name = prompt_str("Name: ", validate=validate_name)
    while True:
        username = prompt_str("Username: ", validate=validate_username)

        if state.username_taken(username):
            _error("Username already taken.")
            press_any_key()
            return None
        break

    while True:
        password = prompt_str("Password: ", hide=True, validate=validate_password)
        confirm = prompt_str("Confirm password: ", hide=True)

        if password == confirm:
            break

        _error("Passwords do not match.")

    while True:
        pin = prompt_str("PIN: ", hide=True, validate=validate_pin)
        confirm = prompt_str("Confirm PIN: ", hide=True)

        if pin == confirm:
            break

        _error("PINs do not match.")

    try:
        state.register(name, username, password, pin)
        print(Fore.GREEN + "Account created." + Style.RESET_ALL)
        press_any_key()
        return True
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
        press_any_key()
        return None


def open_account(state: BankState) -> Any:
    if state.user is None:
        _error("Must be logged in to open an account.")
        return True

    clear()
    print_accounts(state.user)
    title("Open Account")

    while True:
        account_type = prompt_str("Account type (checking/savings): ")
        if account_type not in ("checking", "savings"):
            _error("Invalid account type.")
            continue
        break

    while True:
        name = prompt_str("Account name (optional): ", optional=True)
        if name != "" and not validate_name(name):
            continue
        break

    overdraft_source = None
    if account_type == "checking":
        while True:
            overdraft_source_id = prompt_str(
                "Overdraft source account ID (optional): ", optional=True
            )
            if not overdraft_source_id:
                break
            overdraft_source = state.get_account(overdraft_source_id)
            if not overdraft_source:
                _error("Invalid account ID.")
                continue
            break

    while True:
        password = prompt_str("User account password: ", hide=True)
        if not state.user.login(password):
            _error("Incorrect password.")
            continue
        break

    try:
        state.open_account(account_type, name, overdraft_source)
        print(Fore.GREEN + "Account created." + Style.RESET_ALL)
        press_any_key()
        return True
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
        press_any_key()
        return None


def close_account(state: BankState) -> Any:
    if state.user is None:
        _error("Must be logged in to close an account.")
        return True

    clear()
    print_accounts(state.user)
    title("Close Account")

    if len(state.user.accounts) == 0:
        _error("No accounts to close.")
        press_any_key()
        return True

    while True:
        account_id = prompt_str("Account ID: ")
        account = state.get_account(account_id)
        if not account:
            _error("Invalid account ID.")
            continue
        if account.balance < 0:
            _error("Cannot close account with negative balance.")
            continue
        break

    while True:
        confirm = prompt_str(
            "Are you sure? All funds in the account will be lost. (y/n): ",
            validate=lambda x: x.lower() in ("y", "n"),
        )
        if confirm.lower() == "n":
            return None
        break

    while True:
        password = prompt_str("User account password: ", hide=True)
        if not state.user.login(password):
            _error("Incorrect password.")
            continue
        break

    try:
        state.close_account(account_id)
        print(Fore.GREEN + "Account closed." + Style.RESET_ALL)
        press_any_key()
        return None
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
        press_any_key()
        return None
