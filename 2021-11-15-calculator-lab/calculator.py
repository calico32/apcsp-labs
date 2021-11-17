import sys
from typing import Optional, Union

from colorama import Fore, Style, init  # type: ignore

init()

try:
    import msvcrt
    getch = msvcrt.getch  # type: ignore
except:
    import sys
    import termios
    import tty

    def _unix_getch():
        """Get a single character from stdin, Unix version"""

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())          # Raw read
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    getch = _unix_getch


def error(text: str) -> None:
    """ Print error message """
    print(f"{Fore.RED}{text}{Fore.RESET}")


def prompt(text: str, required=True) -> str:
    """ Print prompt message """
    def get_input(): return input(f"{Fore.BLUE}{text} > {Fore.RESET}")

    if required:
        value = None
        while not value:
            value = get_input()
    else:
        value = get_input()

    return value


def prompt_single(text: str, required=True) -> str:
    """ Print prompt message """
    def get_input():
        print(f"{Fore.BLUE}{text} > {Fore.RESET}", end='', flush=True)
        char = getch()
        print(char)
        return char

    if required:
        value = None
        while not value:
            value = get_input()
    else:
        value = get_input()

    return value


while True:
    try:
        # get the first number
        first_number = float(prompt("Enter a number"))
        # get the operator
        operator = prompt_single("Enter operator [+-*/!^]")

        # check operator
        if operator not in ["+", "-", "*", "/", "!", "^"]:
            error("Invalid operator")
            continue

        result: Optional[Union[float, int]] = None

        if operator == '!':
            if first_number % 1 != 0:
                error('Cannot take factorial of a non-integer')
                print()
                continue

            result = 1
            for i in range(1, int(first_number) + 1):
                result *= i

            print(
                f'{Fore.GREEN}{int(first_number)}! => {Style.BRIGHT}{"{:,}".format(result)}{Fore.RESET}{Style.RESET_ALL}'
            )
            print()
            continue

        # get the second number
        second_number = float(prompt("Enter second number"))

        if operator == "+":
            result = first_number + second_number
        elif operator == "-":
            result = first_number - second_number
        elif operator == "*":
            result = first_number * second_number
        elif operator == '/':
            result = first_number / second_number
        elif operator == "^":
            result = first_number ** second_number

        print(f'{Fore.GREEN}{first_number} {operator} {second_number} => {Style.BRIGHT}{"{:,}".format(result)}{Fore.RESET}{Style.RESET_ALL}')
        print()
    except ValueError:
        error('Invalid number')
        print()
        continue
    except ZeroDivisionError:
        error('Cannot divide by zero')
        print()
        continue
    except (KeyboardInterrupt, EOFError):
        print('\nBye!')
        break
    except Exception as e:
        error('Error encountered:' + str(e))
        print()
        continue
