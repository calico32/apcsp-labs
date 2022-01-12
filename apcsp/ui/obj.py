from abc import ABCMeta
from typing import Type

from colorama import Fore, Style  # type: ignore


class MenuObject(object, metaclass=ABCMeta):
    def __init__(self):
        pass

    def __format__(self, spec: str) -> str:
        return "<unformatted {}>".format(self.__class__.__name__)


class HiddenObject(MenuObject, metaclass=ABCMeta):
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


class Empty(MenuObject):
    def __format__(self, spec: str) -> str:
        return ""


class Text(MenuObject):
    def __init__(self, text: str):
        self.text = text

    def __format__(self, spec: str) -> str:
        return Style.RESET_ALL + self.text + Style.RESET_ALL

    Empty: "Type[Empty]" = Empty
