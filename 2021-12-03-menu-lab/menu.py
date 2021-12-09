import os
from re import A
from typing import Any, Callable, List, Optional, Union

import colorama  # type: ignore
from colorama import Fore, Style
from readchar import readkey  # type: ignore

from _util import (ARROW_DOWN, ARROW_UP, Item, banner, clear, interrupted,
                   print_items)
from checkout import checkout
from menu_edit import menu_add, menu_edit, menu_remove
from order_add import order_add
from order_remove import order_remove
from state import export_state, import_state

colorama.init()

welcomed = False
menu_selected = 0


class MenuOption(object):
    category: str
    name: str

    def __init__(self, category: str, name: str, run: Callable[..., None]):
        self.category = category
        self.name = name
        self.run = run


menu = [
    Item('Chocolate Cake',  650),
    Item('Tiramisu',        1100),
    Item('Coffee',          350),
    Item('Donut',           250),
    Item('Bread',           350),
    Item('Pancakes',        500),
    Item('Cookie',          250),
    Item('Coffee Cake',     400),
    Item('Cupcake',         300),
]

options = [
    MenuOption("Ordering", "Add items to order",
               lambda: order_add(menu)),

    MenuOption("",         "Remove items from order",
               lambda: order_remove(menu)),

    MenuOption("Menu",     "Add menu items",
               lambda: menu_add(menu)),

    MenuOption("",         "Remove menu items",
               lambda: menu_remove(menu)),

    MenuOption("",         "Edit menu items",
               lambda: menu_edit(menu)),

    MenuOption("State",    "Import state from text",
               lambda: import_state(menu)),

    MenuOption("",         "Import state from file",
               lambda: import_state(menu, file=True)),

    MenuOption("",         "Export state to console",
               lambda: export_state(menu)),

    MenuOption("",         "Export state to file",
               lambda: export_state(menu, file=True)),

    MenuOption("Checkout", "Checkout",
               lambda: checkout(menu)),

    MenuOption("",         "Exit",
               lambda: exit_menu()),
]


def print_menu(cls=False, message=None) -> None:
    if cls:
        clear()
        banner(menu)
        print_items(menu)

    if not welcomed:
        print(Fore.GREEN + "Welcome to Copilot Café!" + Style.RESET_ALL)

    if message is not None:
        print(message)

    print(Fore.GREEN + "What would you like to do?" + Style.RESET_ALL)

    previous_category = None
    for index, option in enumerate(options):
        if option.category != previous_category and option.category != "":
            print()
            print(Fore.GREEN + option.category + Style.RESET_ALL)
            previous_category = option.category
        print(
            f"  {Fore.CYAN + Style.BRIGHT + '>' if menu_selected == index else Style.RESET_ALL + ' '} {option.name}{Style.RESET_ALL}"
        )


def exit_menu() -> None:
    global menu_selected
    menu_selected = -1
    print_menu(cls=True)
    exit()


print_menu(cls=True)


while True:
    key = readkey()
    if interrupted(key):
        exit_menu()
    elif key == ARROW_UP:
        menu_selected = (menu_selected - 1) % len(options)
        print_menu(cls=True)
    elif key == ARROW_DOWN:
        menu_selected = (menu_selected + 1) % len(options)
        print_menu(cls=True)
    elif key == '\r':  # enter
        previous_selected = menu_selected
        menu_selected = -1
        print_menu(cls=True)

        menu_selected = previous_selected
        options[menu_selected].run()

        welcomed = True
        print_menu(cls=True)
