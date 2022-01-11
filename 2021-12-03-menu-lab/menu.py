# menu entrypoint

from typing import Callable

import colorama  # type: ignore
from colorama import Fore, Style
from readchar import readkey  # type: ignore

from _util import ARROW_DOWN, ARROW_UP, Item, banner, clear, interrupted, print_items
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
# i guess i have to use a dict somewhere
menu_data = {
    "Chocolate Cake": 650,
    "Tiramisu": 1100,
    "Coffee": 350,
    "Donut": 250,
    "Bread": 350,
    "Pancakes": 500,
    "Cookie": 250,
    "Coffee Cake": 400,
    "Cupcake": 300,
    "Coffee Latte": 450,
    "Cappuccino": 500,
    "Tea": 250,
    "Green Tea": 200,
    "Black Tea": 150,
    "Iced Coffee": 350,
    "Iced Tea": 250,
    "Iced Coffee Latte": 450,
    "Iced Cappuccino": 500,
    "Frozen Yogurt": 300,
    "Frozen Shake": 350,
    "Frozen Pastry": 500,
    "Frozen Smoothie": 600,
    "Frozen Yogurt": 300,
}

menu = [Item(name, menu_data[name]) for name in menu_data]

# main menu options and their associated functions
options = [
    MenuOption("Ordering", "Add items to order", lambda: order_add(menu)),
    MenuOption("", "Remove items from order", lambda: order_remove(menu)),
    MenuOption("Menu", "Add menu items", lambda: menu_add(menu)),
    MenuOption("", "Remove menu items", lambda: menu_remove(menu)),
    MenuOption("", "Edit menu items", lambda: menu_edit(menu)),
    MenuOption("State", "Import state from text", lambda: import_state(menu)),
    MenuOption("", "Import state from file", lambda: import_state(menu, file=True)),
    MenuOption("", "Export state to console", lambda: export_state(menu)),
    MenuOption("", "Export state to file", lambda: export_state(menu, file=True)),
    MenuOption("Checkout", "Checkout", lambda: checkout(menu)),
    MenuOption("", "Exit", lambda: exit_menu()),
]

# print the menu and all the options (selected one highlighted)


def print_menu(message=None) -> None:
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
    print_menu()
    exit()


print_menu()

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
        print_menu()
    elif key == ARROW_DOWN:
        # arrow down
        menu_selected = (menu_selected + 1) % len(options)
        print_menu()
    elif key == "\r":
        # enter
        # clear selected item
        previous_selected = menu_selected
        menu_selected = -1
        print_menu()

        menu_selected = previous_selected
        # run the function for the selected item
        options[menu_selected].run()

        # hide welcome message on next iteration
        welcomed = True
        print_menu()
