from typing import Any

from colorama import Fore, Style  # type: ignore

from ..bank import BankState
from .prompt import _error, press_any_key, prompt_str
from .register import validate_name, validate_password, validate_pin
from .util import clear, print_accounts, title


def change_name(state: BankState) -> Any:
    if state.user is None:
        _error("Must be logged in to change name.")
        return True

    clear()
    print_accounts(state.user)
    title("Change Name")

    new_name = prompt_str(
        "New name (leave blank to cancel): ", validate=validate_name, optional=True
    )
    if new_name is None:
        return True

    try:
        state.user.name = new_name
        print(Fore.GREEN + "Name changed." + Style.RESET_ALL)
        press_any_key()
        return True
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
        press_any_key()
        return False


def change_password(state: BankState) -> Any:
    if state.user is None:
        _error("Must be logged in to change password.")
        return True

    clear()
    print_accounts(state.user)
    title("Change Password")

    current_password = prompt_str("Current password: ", hide=True)
    if not state.user.login(current_password):
        _error("Incorrect password.")
        return True

    while True:
        new_password = prompt_str(
            "New password: ", hide=True, validate=validate_password
        )
        confirm = prompt_str("Confirm password: ", hide=True)

        if new_password != confirm:
            _error("Passwords do not match.")
            return False

        break

    try:
        state.user.set_password(new_password)
        print(Fore.GREEN + "Password changed." + Style.RESET_ALL)
        press_any_key()
        return True
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
        press_any_key()
        return False


def change_pin(state: BankState) -> Any:
    if state.user is None:
        _error("Must be logged in to change PIN.")
        return True

    clear()
    print_accounts(state.user)
    title("Change PIN")

    current_pin = prompt_str("Current PIN: ", hide=True)
    if not state.user.check_pin(current_pin):
        _error("Incorrect PIN.")
        return True

    while True:
        new_pin = prompt_str("New PIN: ", hide=True, validate=validate_pin)
        confirm = prompt_str("Confirm PIN: ", hide=True)

        if new_pin != confirm:
            _error("PINs do not match.")
            return False

        break

    try:
        state.user.set_pin(new_pin)
        print(Fore.GREEN + "PIN changed." + Style.RESET_ALL)
        press_any_key()
        return True
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
        press_any_key()
        return False


def delete_user_account(state: BankState) -> Any:
    if state.user is None:
        _error("Must be logged in to delete account.")
        return True

    clear()
    print_accounts(state.user)
    title("Delete Account")

    confirm = prompt_str(
        "Are you sure you want to delete your account? You will lose access to all your"
        " accounts and funds. (y/n) ",
        validate=lambda x: x in ("y", "n"),
    )
    if confirm == "n":
        return True

    password = prompt_str("Password: ", hide=True)
    if not state.user.login(password):
        _error("Incorrect password.")
        return True

    try:
        state.delete_user_account()
        print(Fore.GREEN + "Account deleted." + Style.RESET_ALL)
        press_any_key()
        return True
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
        press_any_key()
        return False
