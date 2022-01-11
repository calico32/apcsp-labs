from abc import ABC, ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Literal

from colorama import Fore, Style  # type: ignore

from . import action, obj

if TYPE_CHECKING:
    from . import context, menu


class Selectable(obj.MenuObject, metaclass=ABCMeta):
    @abstractmethod
    def select(self, context: "context.MenuContext") -> None:
        pass


class Button(Selectable):
    def __init__(
        self,
        label: str,
        *,
        run: Callable[..., Any] = lambda: None,
        type: action.ActionType | None = None,
    ):
        self.label = label
        self.run = run
        self.type = type

    def select(self, context: "context.MenuContext") -> None:
        if self.run is not None:
            self.run(context)

        if self.type in ("_exit", "_interrupt"):
            context.exit()  # type: ignore # TODO

    def __format__(self, spec: str) -> str:
        return "{color}{caret} {reset} {label}{reset}".format(
            color=Fore.CYAN + Style.BRIGHT,
            caret=">" if spec.split(",")[0] == ">" else " ",
            label=self.label,
            reset=Style.RESET_ALL,
        )


class Submenu(Button):
    def __init__(self, label: str, menu: "menu.Menu"):
        super().__init__(label, run=lambda context: menu.run(context))


class Exit(Button):
    def __init__(self, label="Exit"):
        super().__init__(label, type="_exit")
