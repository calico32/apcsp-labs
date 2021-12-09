from enum import Enum
from typing import List, NewType

from colorama import Fore, Style  # type: ignore
from readchar import readkey  # type: ignore

from _prompt import prompt_index, prompt_name, prompt_price
from _util import (ARROW_DOWN, ARROW_UP, Item, banner, clear, interrupted,
                   print_items)


class EditMode(Enum):
    ADD = 1
    REMOVE = 2
    EDIT = 3


def edit_items(menu: List[Item], mode: EditMode) -> None:
    clear()
    banner(menu)

    if mode == EditMode.ADD:
        _edit_add(menu)
    elif mode == EditMode.REMOVE:
        _edit_remove(menu)
    elif mode == EditMode.EDIT:
        _edit_item(menu)


def _edit_add(menu: List[Item]) -> None:
    print_items(menu)

    print(Fore.CYAN + Style.BRIGHT +
          "Adding menu item (Ctrl+C to return)" + Style.RESET_ALL)

    try:
        name = prompt_name("Enter item name: ")
        price = prompt_price("Enter item price: ")
        index = prompt_index(menu, "Enter item index: ")

        menu.insert(index, Item(name, price))
    except KeyboardInterrupt:
        return


def _edit_remove(menu: List[Item]) -> None:
    selected = 0

    def print_menu(cls=False) -> None:
        if cls:
            clear()
            banner(menu)

        print_items(menu, selected)

        print(Fore.CYAN + Style.BRIGHT +
              "Removing menu item (Ctrl+C to return)" + Style.RESET_ALL)

        print(Fore.GREEN + "Select the item you would like to remove." + Style.RESET_ALL)

    print_menu(cls=True)

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
            menu.remove(menu[selected])
            return


def _edit_item(menu):
    print_items(menu)

    selected = 0

    def print_menu(cls=False) -> None:
        if cls:
            clear()
            banner(menu)

        print_items(menu, selected)

        print(Fore.CYAN + Style.BRIGHT +
              "Editing menu item (Ctrl+C to return)" + Style.RESET_ALL)

        print(Fore.GREEN + "Select the item you would like to edit." + Style.RESET_ALL)

    print_menu(cls=True)

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
            _edit_item_prompt(menu, selected)
            print_menu(cls=True)


def _edit_item_prompt(menu: List[Item], index: int) -> None:
    item = menu[index]

    def options():
        return [
            'Name: ' + item.name,
            'Price: ' + item.price_formatted,
            'Index: ' + str(index),
        ]

    selected = 0

    def editing_message():
        return f"{Fore.CYAN}{Style.BRIGHT}Editing item: {item.name} (Ctrl+C to return) {Style.RESET_ALL}"

    def print_options(edit_index: int) -> None:
        clear()
        banner(menu)
        print_items(menu, edit_index)

        print(editing_message())

        print(Fore.GREEN + 'Select the property you would like to edit.' + Style.RESET_ALL)

        for index, option in enumerate(options()):
            print(
                f"  {Fore.CYAN + Style.BRIGHT + '>' if selected == index else Style.RESET_ALL + ' '} {option}"
            )

    print_options(index)

    try:
        while True:
            key = readkey()
            if interrupted(key):
                return
            elif key == ARROW_UP:  # up arrow
                selected = (selected - 1) % len(options())
                print_options(index)
            elif key == ARROW_DOWN:  # down arrow
                selected = (selected + 1) % len(options())
                print_options(index)
            elif key == '\r':  # enter
                clear()
                banner(menu)
                print_items(menu, index)
                print(editing_message())
                if selected == 0:
                    item.name = prompt_name("Enter item name: ")
                elif selected == 1:
                    item.price = prompt_price("Enter item price: ")
                elif selected == 2:
                    new_index = prompt_index(
                        menu, "Enter item index: ", allow_overflow=False)
                    menu.remove(item)
                    menu.insert(new_index, item)
                    index = new_index
                print_options(index)
    except KeyboardInterrupt:
        return
