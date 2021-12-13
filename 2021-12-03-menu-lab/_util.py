# helpers, utilities, constants, etc.

import os
from typing import List, Tuple

from colorama import Fore, Style  # type: ignore

# currency symbol used in the menu
CURRENCY = '₿'

# arrow key escape sequences
ARROW_UP = '\x1b[A'
ARROW_DOWN = '\x1b[B'


# item class, used to store item information and count
class Item:
    name: str
    price: int
    count: int

    def __init__(self, name: str, price: int, count=0):
        self.name = name
        self.price = price
        self.count = count

    @property
    def price_formatted(self) -> str:
        return f"{self.price / 100:.2f} {CURRENCY}"

    @property
    def subtotal(self) -> int:
        return self.price * self.count

    @property
    def subtotal_formatted(self) -> str:
        return f"{self.subtotal / 100:.2f} {CURRENCY}"


# get the widths of the columns
def widths(menu: List[Item]) -> Tuple[int, int, int, int]:
    index = len(str(len(menu))) + 1
    name = max(len(item.name) for item in menu)
    price = max(len(item.price_formatted) for item in menu)
    quantity = max(len(str(item.count)) for item in menu)
    return max(index, 3), max(name, 4), max(price, 5), max(quantity, 3)


# total width of the menu
def width(menu: List[Item]) -> int:
    index, name, price, quantity = widths(menu)
    return index + 2 + name + 2 + price + 2 + quantity

# columns for the table


def columns(menu: List[Item]) -> str:
    index, name, price, quantity = map(str, widths(menu))
    return f'{{:<{index}}}  {{:<{name}}}  {{:>{price}}}  {{:>{quantity}}}'


# clear the screen
def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


# print a separator
def separator(menu: List[Item]) -> None:
    print(Style.RESET_ALL, end='')
    print('-' * width(menu))


# menu banner
def banner(menu: List[Item]) -> None:
    print(Style.RESET_ALL, end='')
    separator(menu)
    print(Fore.BLUE + Style.BRIGHT + 'Copilot Cafe™' + Style.RESET_ALL)


# print items and prices in a table
def print_items(menu: List[Item], selected=None) -> None:
    print(Style.RESET_ALL, end='')
    print(columns(menu).format('#', 'Item', 'Price', 'Qty'))
    separator(menu)

    # print each item and price with an index
    for index, item in enumerate(menu):
        line = columns(menu).format(
            str(index) + '.',
            item.name,
            item.price_formatted,
            item.count
        )

        if selected == index:
            print(Fore.CYAN + Style.BRIGHT, end='')
            line = line[:3] + '*' + line[4:] + Style.RESET_ALL
        elif item.count > 0:
            line = Fore.BLUE + line + Style.RESET_ALL

        print(line)

    separator(menu)


# keypresses used for exiting current menu
def interrupted(key: str) -> bool:
    return key in ['q', 'Q', '\x1b', '\x1b\x1b', '\x03', '\x04']
