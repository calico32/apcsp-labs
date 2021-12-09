from typing import List

from colorama import Fore, Style  # type: ignore
from readchar import readkey  # type: ignore

from _util import (ARROW_DOWN, ARROW_UP, Item, banner, clear, interrupted,
                   print_items)


def order_remove(menu: List[Item]) -> None:
    clear()
    banner(menu)

    selected = 0

    def print_menu(cls=False):
        if cls:
            clear()
            banner(menu)

        print_items(menu, selected)

        print(Fore.CYAN + Style.BRIGHT +
              "Removing items from your order (Ctrl+C to return)" + Style.RESET_ALL)

        print(Fore.GREEN + "Select the item you would like to remove." + Style.RESET_ALL)

    print_menu()

    while True:
        key = readkey()
        if interrupted(key):
            return
        elif key == ARROW_UP:  # up arrow
            selected = (selected - 1) % len(menu)
            print_menu(cls=True)
        elif key == ARROW_DOWN:  # down arrow
            selected = (selected + 1) % len(menu)
            print_menu(cls=True)
        elif key == '\r':  # enter
            _prompt_quantity(menu, selected)
            return


def _prompt_quantity(menu: List[Item], selected: int) -> None:
    clear()
    banner(menu)

    print_items(menu, selected)

    quantity = None
    try:
        while quantity is None:
            try:
                value = int(
                    input(Fore.GREEN + "Enter quantity to remove: " + Style.RESET_ALL))
                if value < 0 or value > menu[selected].count:
                    raise ValueError
                quantity = value
            except ValueError:
                print(
                    Fore.RED + "Invalid quantity. Please enter a positive integer less than or equal to the number of items in your order." + Style.RESET_ALL
                )

        menu[selected].count -= quantity
    except KeyboardInterrupt:
        return
