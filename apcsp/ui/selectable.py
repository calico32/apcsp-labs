from abc import ABC, ABCMeta, abstractmethod
from functools import partialmethod
from inspect import getfullargspec
from typing import TYPE_CHECKING, Any, Callable, Dict, Literal, Type

from apcsp.ui import obj
from colorama import Fore, Style  # type: ignore

if TYPE_CHECKING:
    from apcsp.ui import context, form, menu

FormResult = Dict[str, "form.FormField"]


class Selectable(obj.MenuObject, metaclass=ABCMeta):
    @abstractmethod
    def select(self, ctx: "context.MenuContext") -> None:
        pass


class Button(Selectable):
    def __init__(
        self,
        label: str,
        *,
        run: "Callable[[], Any] | Callable[[context.MenuContext], Any] | None" = None,
    ):
        self.label = label
        self.run = run
        self.type = type

    def select(self, ctx: "context.MenuContext") -> None:
        if self.run is None and self.type is None:
            print("WARNING: Button has no action")

        if self.run is not None:
            spec = getfullargspec(self.run)
            if len(spec.args) == 0:
                self.run()  # type: ignore
            elif len(spec.args) == 1:
                self.run(ctx)  # type: ignore
            else:
                raise ValueError(
                    "Button run function must take 0 or 1 argument ("
                    + ",".join(spec.args)
                    + ")"
                )

        if self.type in ("_interrupt", "_cancel"):
            ctx.exit()

    def __format__(self, spec: str) -> str:
        return "{color}{caret} {label}{reset}".format(
            color=Fore.CYAN + Style.BRIGHT,
            caret=">" if spec.split(",")[1] == ">" else " " + Style.RESET_ALL,
            label=self.label,
            reset=Style.RESET_ALL,
        )

    Cancel: "Type[Cancel]"
    Submit: "Type[Submit]"
    Exit: "Type[Exit]"
    Submenu: "Type[Submenu]"


class Submenu(Button):
    def __init__(self, label: str, menu: "menu.Menu"):
        self.menu = menu
        super().__init__(label, run=lambda ctx: self.open_menu(ctx))  # type: ignore

    def open_menu(self, ctx: "context.MenuContext") -> None:
        ctx = ctx.fork(self.menu)
        ctx.run()


class Cancel(Button):
    def __init__(self, label: str = "Cancel"):
        super().__init__(label, run=lambda ctx: ctx.exit())


class Submit(Button):
    def __init__(
        self,
        label: str = "Submit",
        on_submit: "Callable[[context.MenuContext, FormResult], Any]" = lambda ctx, data: None,
    ):
        super().__init__(label, run=lambda ctx: self.submit(ctx))
        self.on_submit = on_submit

    def submit(self, ctx: "context.MenuContext") -> None:
        data = ctx.submit()
        if data is not None:
            self.on_submit(ctx, data)


class Exit(Button):
    def __init__(self, label="Exit"):
        super().__init__(label, run=lambda ctx: ctx.exit())


Button.Cancel = Cancel
Button.Submit = Submit
Button.Exit = Exit
Button.Submenu = Submenu
