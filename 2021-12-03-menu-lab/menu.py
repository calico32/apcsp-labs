import os
from typing import Callable, List, Union

import colorama  # type: ignore
from colorama import Fore, Style
from readchar import readkey  # type: ignore

from checkout import checkout
from edit import EditMode, edit_items
from order_add import order_add
from order_remove import order_remove
from state import export_state, import_state
from _util import (ARROW_DOWN, ARROW_UP, Item, banner, clear, interrupted,
                   print_items)

colorama.init()


menu = [
    Item('Chocolate Cake', 650),
    Item('Tiramisu', 1100),
    Item('Coffee', 350),
    Item('Donut', 250),
    Item('Bread', 350),
    Item('Pancakes', 500),
    Item('Cookie', 250),
    Item('Coffee Cake', 400),
    Item('Cupcake', 300),
]


class MenuOption(object):
    category: str
    name: str

    def __init__(self, category: str, name: str, run: Callable[..., None]):
        self.category = category
        self.name = name
        self.run = run


def menu_order_add(_, __): order_add(menu)
def menu_order_remove(_, __): order_remove(menu)
def menu_edit_add(_, __): edit_items(menu, EditMode.ADD)


def menu_edit_remove(print_menu: Callable, __):
    if len(menu) == 1:
        print_menu(
            cls=True, message=f"{Fore.RED}You must have at least one item in the menu!{Style.RESET_ALL}")
    edit_items(menu, EditMode.REMOVE)


def menu_edit_edit(_, __): edit_items(menu, EditMode.EDIT)
def menu_import_console(_, __): import_state(menu)
def menu_import_file(_, __): import_state(menu, file=True)
def menu_export_console(_, __): export_state(menu)
def menu_export_file(_, __): export_state(menu, file=True)


def menu_checkout(print_menu: Callable, __):
    if len(list(filter(lambda item: item.count > 0, menu))) == 0:
        print_menu(
            cls=True, message=f"{Fore.RED}You must have at least one item in your order!{Style.RESET_ALL}",)
    checkout(menu)


def menu_exit(_, exit_menu: Callable): exit_menu()


welcomed = False

menu_selected = 0

options = [
    MenuOption("Ordering", "Add items to order",      menu_order_add),
    MenuOption("",         "Remove items from order", menu_order_remove),
    MenuOption("Menu",     "Add menu items",          menu_edit_add),
    MenuOption("",         "Remove menu items",       menu_edit_remove),
    MenuOption("",         "Edit menu items",         menu_edit_edit),
    MenuOption("State",    "Import state from text",  menu_import_console),
    MenuOption("",         "Import state from file",  menu_import_file),
    MenuOption("",         "Export state to console", menu_export_console),
    MenuOption("",         "Export state to file",    menu_export_file),
    MenuOption("Checkout", "Checkout",                menu_checkout),
    MenuOption("",         "Exit",                    menu_exit),
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


def exit_menu(actually_exit=True):
    global menu_selected
    menu_selected = -1
    print_menu(cls=True)
    if actually_exit:
        exit()


print_menu(cls=True)

while True:
    key = readkey()
    if interrupted(key):
        exit_menu()
    elif key == ARROW_UP:  # up arrow
        menu_selected = (menu_selected - 1) % len(options)
        print_menu(cls=True)
    elif key == ARROW_DOWN:  # down arrow
        menu_selected = (menu_selected + 1) % len(options)
        print_menu(cls=True)
    elif key == '\r':  # enter
        options[menu_selected].run(print_menu, exit_menu)
        welcomed = True
        print_menu(cls=True)
