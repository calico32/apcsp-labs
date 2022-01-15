# helpers, utilities, constants, etc.

import os
from typing import Any, Callable, Final, List, Tuple

from colorama import Fore, Style  # type: ignore
from readchar import readkey  # type: ignore

from ..account_types import UserAccount, UserHoldableAccount
from ..bank import BankState

# arrow key escape sequences
ARROW_UP: Final[str] = "\x1b[A"
ARROW_DOWN: Final[str] = "\x1b[B"


class MenuOption(object):
    category: str
    name: str

    def __init__(self, category: str, name: str, run: Callable[[BankState], Any]):
        self.category = category
        self.name = name
        self.run = run


# get the widths of the columns
def widths(user: UserAccount) -> Tuple[int, int, int]:
    id = max(len(str(account.id)) for account in user.accounts) if user.accounts else 0
    name = max(len(account.name) for account in user.accounts) if user.accounts else 0
    bal = (
        max(len(account.balance_str) for account in user.accounts)
        if user.accounts
        else 0
    )
    return max(id, 2), max(name, 10), max(bal, 8)


# total width of the menu
def width(user: UserAccount) -> int:
    id, name, bal = widths(user)
    return id + 2 + name + 2 + bal


# columns for the table
def columns(user: UserAccount) -> str:
    id, name, bal = map(str, widths(user))
    return f"{{:<{id}}}  {{:<{name}}}  {{:>{bal}}}"


# clear the screen
def clear(use_ansi: bool = False) -> None:
    if use_ansi:
        # move to top left
        print("\x1b[H", end="")
    else:
        os.system("cls" if os.name == "nt" else "clear")


# print a separator
def separator(user: UserAccount) -> None:
    print(Style.RESET_ALL, end="")
    print("-" * width(user))


# menu banner
def banner(user: UserAccount) -> None:
    print(Style.RESET_ALL, end="")
    separator(user)
    print(Fore.BLUE + Style.BRIGHT + f"{user.name} ({user.id})" + Style.RESET_ALL)


def title(title: str) -> None:
    print(Fore.CYAN + Style.BRIGHT + title + Style.RESET_ALL)


# print items and prices in a table
def print_accounts(user: UserAccount, selected: int | None = None) -> None:
    banner(user)
    cols = columns(user)

    if len(user.accounts) == 0:
        print(cols.format("  No accounts", "", ""))
        separator(user)
        return

    print(Style.RESET_ALL, end="")
    print(cols.format("ID", "Name", "Balance"))

    separator(user)

    # print each item and price with an index
    for index, acc in enumerate(user.accounts):
        line = cols.format(acc.id, acc.name, acc.balance_str)

        if selected == index:
            print(Fore.CYAN + Style.BRIGHT, end="")
            line = line[:3] + "*" + line[4:] + Style.RESET_ALL
        elif acc.balance > 0:
            line = Fore.GREEN + line + Style.RESET_ALL
        elif acc.balance < 0:
            line = Fore.RED + line + Style.RESET_ALL

        print(line)

    separator(user)


# keypresses used for exiting current menu
def interrupted(key: str) -> bool:
    return key in ["q", "Q", "\x1b", "\x1b\x1b", "\x03", "\x04"]


def menu(
    state: BankState,
    options: List[MenuOption],
    message: str = "",
) -> Tuple[int, str, Any] | None:
    selected = 0

    def print_menu() -> None:
        clear()

        if state.user:
            print_accounts(state.user)

        if message:
            print(message)

        print(Fore.GREEN + "What would you like to do?" + Style.RESET_ALL)

        previous_category = None
        for index, option in enumerate(options):
            if option.category != previous_category and option.category != "":
                print()
                print(Fore.GREEN + option.category + Style.RESET_ALL)
                previous_category = option.category
            print(
                f"  {Fore.CYAN + Style.BRIGHT + '>' if selected == index else Style.RESET_ALL + ' '} {option.name}{Style.RESET_ALL}"
            )

    print_menu()

    # menu loop
    while True:
        # get one keypress
        key = readkey()
        if interrupted(key):
            return 0, "", "_exit"
        elif key == ARROW_UP:
            # arrow up
            selected = (selected - 1) % len(options)
            print_menu()
        elif key == ARROW_DOWN:
            # arrow down
            selected = (selected + 1) % len(options)
            print_menu()
        elif key == "\r":
            # enter
            # clear selected item
            previous_selected = selected
            selected = -1
            print_menu()

            selected = previous_selected
            val = options[selected].run(state)
            if val is not None:
                name = options[selected].name
                return selected, name, val
            selected = previous_selected

            print_menu()
