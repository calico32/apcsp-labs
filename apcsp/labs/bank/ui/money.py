from colorama import Fore, Style  # type: ignore

from ..account import format_name
from ..bank import BankState
from ..util import format_amount
from .prompt import _error, press_any_key, prompt_float, prompt_str
from .util import clear, print_accounts, title


def is_positive(val: str) -> bool:
    try:
        f = float(val)
        if f < 0:
            _error("Amount must be positive.")
            return False
    except ValueError:
        _error("Amount must be a number.")
        return False

    return True


def deposit(state: BankState):
    if state.user is None:
        _error("Must be logged in to deposit.")
        return True

    clear()
    print_accounts(state.user)
    title("Deposit")

    if len(state.user.accounts) == 0:
        _error("No accounts to deposit to. Create one first.")
        press_any_key()
        return True

    amount = prompt_float("Amount: ", validate=is_positive)
    desc = prompt_str("Description (leave blank for none): ", optional=True)
    while True:
        account_id = prompt_str("Account ID: ")
        account = state.get_account(account_id)
        if not account:
            _error("Invalid account ID.")
            continue
        break

    while True:
        pin = prompt_str("PIN: ", hide=True)
        if not state.user.check_pin(pin):
            _error("Invalid PIN.")
            continue
        break

    try:
        account.deposit(int(amount * 100), desc or None)
        print(
            Fore.GREEN
            + "Deposit of"
            f" {format_amount(int(amount * 100), include_sign=False)} successful."
            + Style.RESET_ALL
        )
        press_any_key()
        return True
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
        press_any_key()
        return False


def withdraw(state: BankState):
    if state.user is None:
        _error("Must be logged in to withdraw.")
        return True

    clear()
    print_accounts(state.user)
    title("Withdraw")

    if len(state.user.accounts) == 0:
        _error("No accounts to withdraw from. Create one first.")
        press_any_key()
        return True

    while True:
        account_id = prompt_str("Account ID: ")
        account = state.get_account(account_id)
        if not account:
            _error("Invalid account ID.")
            continue
        break

    amount = prompt_float("Amount: ", validate=is_positive)
    desc = prompt_str("Description (leave blank for none): ", optional=True)

    while True:
        pin = prompt_str("PIN: ", hide=True)
        if not state.user.check_pin(pin):
            _error("Invalid PIN.")
            continue
        break

    try:
        account.withdraw(int(amount * 100), desc or None)
        print(
            Fore.GREEN
            + "Withdrawal of"
            f" {format_amount(int(amount * 100), include_sign=False)} successful."
            + Style.RESET_ALL
        )
        press_any_key()
        return True
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
        press_any_key()
        return False


def transfer(state: BankState):
    if state.user is None:
        _error("Must be logged in to transfer.")
        press_any_key()
        return True

    clear()
    print_accounts(state.user)
    title("Transfer")

    if len(state.user.accounts) == 0:
        _error("No accounts to transfer from. Create one first.")
        press_any_key()
        return True

    while True:
        source_id = prompt_str("Source account ID: ")
        source = state.get_account(source_id)
        if not source:
            _error("Invalid source account ID.")
            continue
        break

    while True:
        dest_id = prompt_str("Destination account ID: ")
        dest = state.find_account(dest_id)
        if not dest:
            _error("Invalid destination account ID.")
            continue

        if dest == source:
            _error("Source and destination accounts must be different.")
            continue

        if source._owner != dest._owner:
            confirm = prompt_str(
                f"Destination account is {format_name(dest, source)}. Confirm? (y/n) ",
                validate=lambda x: x in ("y", "n"),
            )

            if confirm != "y":
                continue

        break

    amount = prompt_float("Amount: ", validate=is_positive)
    confirm = prompt_str(
        f"Transfer {format_amount(int(amount * 100))} to {format_name(source, dest)}?"
        " (y/n) ",
        validate=lambda x: x in ("y", "n"),
    )

    if confirm != "y":
        _error("Transfer cancelled.")
        press_any_key()
        return True

    while True:
        pin = prompt_str("PIN: ", hide=True)
        if not state.user.check_pin(pin):
            _error("Invalid PIN.")
            continue
        break

    try:
        source.transfer(dest, int(amount * 100))
        print(
            Fore.GREEN
            + f"Transfer of {format_amount(int(amount * 100))} to"
            f" {format_name(source, dest)} successful."
            + Style.RESET_ALL
        )
        press_any_key()
        return True
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
        press_any_key()
        return False


def view_transactions(state: BankState):
    if state.user is None:
        _error("Must be logged in to view transactions.")
        return True

    clear()
    print_accounts(state.user)
    title("View Transactions")

    if len(state.user.accounts) == 0:
        _error("No accounts to view transactions from. Create one first.")
        press_any_key()
        return True

    while True:
        account_id = prompt_str("Account ID: ")
        account = state.get_account(account_id)
        if not account:
            _error("Invalid account ID.")
            continue
        break

    while True:
        pin = prompt_str("PIN: ", hide=True)
        if not state.user.check_pin(pin):
            _error("Invalid PIN.")
            continue
        break

    try:
        print()
        print(account.transactions_str())
        press_any_key()
        return True
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
        press_any_key()
        return False
