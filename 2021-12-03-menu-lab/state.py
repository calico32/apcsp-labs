
from re import M, match
from typing import List, final

from colorama import Fore, Style  # type: ignore
from readchar import readkey  # type: ignore

from prompt import prompt_file
from util import Item


def export_state(menu: List[Item], file=False) -> None:
    print()
    print(Fore.GREEN + 'Exporting state as CSV...' + Style.RESET_ALL)
    csv = 'item_name,item_price,item_count\n'

    for item in menu:
        csv += f'{item.name},{item.price},{item.count}\n'

    if file:
        filename = prompt_file("Enter output filename: ")

        with open(filename, "w") as f:
            f.write(csv)

        print(Fore.GREEN + 'State exported to ' + filename + Style.RESET_ALL)

    else:
        print()
        print(csv)

    print()
    print(Fore.GREEN + "Press any key to continue" + Style.RESET_ALL)
    while True:
        key = readkey()
        if key:
            break


def import_state(menu: List[Item], file=False) -> None:
    print()

    if file:
        filename = prompt_file("Enter input filename: ")

        try:
            with open(filename, "r") as f:
                csv = f.read()
        except FileNotFoundError:
            print(Fore.RED + 'Error: Invalid file' + Style.RESET_ALL)
    else:
        csv = input(
            Fore.GREEN + "Enter CSV (empty line to stop): " + Style.RESET_ALL) + '\n'
        while (line := input(Fore.GREEN + '> ' + Style.RESET_ALL)).strip() != '':
            csv += line + '\n'

    print('-')
    print(csv)
    print('-')

    saved_state = menu.copy()
    try:
        lines = csv.split('\n')
        menu.clear()
        for line in lines:
            if match(r'^item.+?,item.+?,item.+$', line) or line.strip() == '':
                continue

            name, price, count = line.split(',')
            menu.append(Item(name, int(price), int(count)))

    except Exception as e:
        print(Fore.RED + 'Error: ' + str(e) + Style.RESET_ALL)
        menu.clear()
        menu.extend(saved_state)
    # except Exception:
        # print(Fore.RED + 'Error: Unknown' + Style.RESET_ALL)
        # menu.clear()
        # menu.extend(saved_state)

    if file:
        print(Fore.GREEN + 'State imported from ' +
              filename + Style.RESET_ALL)
    else:
        print(Fore.GREEN + 'State imported' + Style.RESET_ALL)

    print()
    print(Fore.GREEN + "Press any key to continue" + Style.RESET_ALL)
    while True:
        key = readkey()
        if key:
            break
