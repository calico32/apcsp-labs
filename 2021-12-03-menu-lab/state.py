# program state import/export

from re import match
from typing import List

from colorama import Fore, Style  # type: ignore

from _prompt import _error, press_any_key, prompt_file
from _util import Item


# export current program state to CSV file (or stdout)
def export_state(menu: List[Item], file=False) -> None:
    try:
        print()
        print(Fore.GREEN + "Exporting state as CSV..." + Style.RESET_ALL)
        csv = "item_name,item_price,item_count\n"

        for item in menu:
            csv += f"{item.name},{item.price},{item.count}\n"

        if file:
            filename = prompt_file("Enter output filename: ")

            with open(filename, "w") as f:
                f.write(csv)

            print(Fore.GREEN + "State exported to " + filename + Style.RESET_ALL)

        else:
            print()
            print(csv)

        press_any_key()
    except KeyboardInterrupt:
        return


# import CSV file to current program state, overwriting current state


def import_state(menu: List[Item], file=False) -> None:
    saved_state = menu.copy()
    try:
        print()

        if file:
            filename = prompt_file("Enter input filename: ")

            try:
                with open(filename, "r") as f:
                    csv = f.read()
            except FileNotFoundError:
                _error("Error: Invalid file")
                press_any_key()
                return
        else:
            csv = (
                input(Fore.GREEN + "Enter CSV (empty line to stop): " + Style.RESET_ALL)
                + "\n"
            )
            done = False
            while not done:
                line = input(Fore.GREEN + "> " + Style.RESET_ALL).strip()
                if line == "":
                    done = True
                else:
                    csv += line + "\n"

        print("-")
        print(csv)
        print("-")

        try:
            lines = csv.split("\n")
            menu.clear()
            for line in lines:
                if match(r"^item.+?,item.+?,item.+$", line) or line.strip() == "":
                    continue

                name, price, count = line.split(",")
                menu.append(Item(name, int(price), int(count)))

        except Exception as e:
            print(Fore.RED + "Error: " + str(e) + Style.RESET_ALL)
            # operation failed, restore previous state
            menu.clear()
            menu.extend(saved_state)

        if file:
            print(Fore.GREEN + "State imported from " + filename + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "State imported" + Style.RESET_ALL)

        press_any_key()
    except KeyboardInterrupt:
        # operation cancelled, restore original state
        menu.clear()
        menu.extend(saved_state)
        return
