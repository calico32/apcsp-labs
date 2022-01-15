from getpass import getpass
from math import nan
from typing import Callable, List, Literal, overload

from colorama import Fore, Style  # type: ignore
from readchar import readkey  # type: ignore


# generic error message
def _error(message: str) -> None:
    """Print error message in red"""
    print(Fore.RED + message + Style.RESET_ALL)


# green prompt message
def _prompt(message: str, hide: bool = False) -> str:
    formatted = Fore.GREEN + message + Style.RESET_ALL
    if hide:
        return getpass(formatted)
    else:
        return input(formatted)


def prompt_str(
    message: str,
    validate: Callable[[str], bool] = lambda value: True,
    hide: bool = False,
    optional: bool = False,
) -> str:
    ret: str | None = None
    while ret is None:
        value = _prompt(message, hide=hide)

        if not value.strip():
            if optional:
                return ""
            continue
        if not validate(value):
            continue

        ret = value

    return ret


def prompt_float(
    message: str,
    validate: Callable[[str], bool] = lambda value: True,
    optional: bool = False,
) -> float:
    ret = None
    while ret is None:
        value = _prompt(message)
        if value.strip() == "":
            if optional:
                return nan
            continue
        else:
            try:
                f = float(value)
                if not validate(value):
                    continue
                ret = f
            except ValueError:
                _error("Invalid number.")
                continue
    return f


# press any key to continue prompt
def press_any_key(message="Press any key to continue") -> None:
    print()
    print(Fore.GREEN + message + Style.RESET_ALL)
    while True:
        key = readkey()
        if key:
            break
