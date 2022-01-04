# input prompting and validation

from typing import List

from colorama import Fore, Style  # type: ignore
from readchar import readkey  # type: ignore

from _util import Item


# generic error message
def _error(message: str) -> None:
    """Print error message in red"""
    print(Fore.RED + message + Style.RESET_ALL)


# green prompt message
def _prompt(message: str) -> str:
    return input(Fore.GREEN + message + Style.RESET_ALL)


# prompt for item name
def prompt_name(message: str) -> str:
    name = None
    while name is None:
        name = _prompt(message)
        if name.strip() == "":
            name = None
        elif name is not None and len(name) > 30:
            _error("Name must be 30 characters or less.")
            name = None
        if name is not None and "," in name:
            _error("Name cannot contain commas.")
            name = None

    return name


# prompt for item price
def prompt_price(message: str) -> int:
    """Prompt for item price and return cents"""
    price = None
    while price is None:
        value = _prompt(message)
        if value == "":
            price = None
        elif value is not None and not value.replace(".", "").isdecimal():
            _error("Price must be a positive number.")
            price = None
        else:
            try:
                price = int(float(value) * 100)
            except ValueError:
                _error("Price must be a positive number.")
                price = None
    return price


# prompt for item index
def prompt_index(menu: List[Item], message: str, allow_overflow=True) -> int:
    index = None
    while index is None:
        value = _prompt(message)
        if value == "":
            index = None
        elif value is not None and not value.isnumeric():
            _error("Index must be a number.")
            index = None
        else:
            index = int(value)
            over_max = index > len(menu) if allow_overflow else index >= len(menu)
            if index < 0 or over_max:
                _error(
                    "Index must be between 0 and"
                    f" {len(menu) if allow_overflow else len(menu) - 1}."
                )
                index = None
    return index


# prompt for file name
def prompt_file(message: str) -> str:
    file = None
    while file is None:
        file = _prompt(message)
        if file.strip() == "":
            file = None
        elif file is not None and not file.endswith(".csv"):
            _error("File must be a .csv file.")
            file = None
    return file


# press any key to continue prompt
def press_any_key(message="Press any key to continue") -> None:
    print()
    print(Fore.GREEN + message + Style.RESET_ALL)
    while True:
        key = readkey()
        if key:
            break
