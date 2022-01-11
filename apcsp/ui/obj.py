from colorama import Fore, Style  # type: ignore


class MenuObject(object):
    def __init__(self):
        pass


class Title(MenuObject):
    def __init__(self, title: str):
        self.title = title

    def __format__(self, spec: str) -> str:
        return Fore.BLUE + Style.BRIGHT + self.title + Style.RESET_ALL


class Category(MenuObject):
    def __init__(self, name: str):
        self.name = name

    def __format__(self, spec: str) -> str:
        return Fore.GREEN + self.name + Style.RESET_ALL
