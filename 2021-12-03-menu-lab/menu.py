# menu entrypoint

from typing import Callable

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


# default menu items
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

# main menu options and their associated functions
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

# print the menu and all the options (selected one highlighted)


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

# set menu_selected to -1 and reprint the menu so that nothing is highlighted
# exit


def exit_menu() -> None:
    global menu_selected
    menu_selected = -1
    print_menu(cls=True)
    exit()


print_menu(cls=True)

# menu loop
while True:
    # get one keypress
    key = readkey()
    if interrupted(key):
        # ctrl-c, ctrl-d, q, or esc
        exit_menu()
    elif key == ARROW_UP:
        # arrow up
        menu_selected = (menu_selected - 1) % len(options)
        print_menu(cls=True)
    elif key == ARROW_DOWN:
        # arrow down
        menu_selected = (menu_selected + 1) % len(options)
        print_menu(cls=True)
    elif key == '\r':
        # enter
        # clear selected item
        previous_selected = menu_selected
        menu_selected = -1
        print_menu(cls=True)

        menu_selected = previous_selected
        # run the function for the selected item
        options[menu_selected].run()

        # hide welcome message on next iteration
        welcomed = True
        print_menu(cls=True)
