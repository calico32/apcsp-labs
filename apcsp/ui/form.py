from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any, List, Type

from apcsp.ui import selectable, util, validation
from colorama import Fore, Style  # type: ignore

if TYPE_CHECKING:
    from apcsp.ui import context


class KeyReceiver(metaclass=ABCMeta):
    @abstractmethod
    def on_key(self, key: str, ctx: "context.MenuContext") -> None:
        pass


class FormField(selectable.Selectable, KeyReceiver, metaclass=ABCMeta):
    error: str | None
    value: Any

    def __init__(self, id: str) -> None:
        self.id = id
        self.error = None

    def _format_error(self, selected: bool) -> str:
        return (
            (Fore.RED + Style.BRIGHT + "! " + self.error + " " + Style.RESET_ALL)
            if self.error
            else ""
        ) + ((Fore.CYAN + Style.BRIGHT) if selected else "")

    def validate(self) -> bool:
        return True

    Select: "Type[SelectField]"
    Text: "Type[TextField]"
    Numeric: "Type[NumericField]"
    Password: "Type[PasswordField]"


class SelectField(FormField):
    def __init__(self, id: str, prompt: str, choices: List[str]):
        super().__init__(id)
        self.prompt = prompt
        self.choices = choices
        self.selected = 0

    value = property(lambda self: self.choices[self.selected])

    def select(self, ctx: "context.MenuContext") -> None:
        pass

    def on_key(self, key: str, ctx: "context.MenuContext") -> None:
        clear = False

        if key == util.ARROW_RIGHT:
            if self.error:
                self.error = None
                clear = True
            self.selected = (self.selected + 1) % len(self.choices)
        elif key == util.ARROW_LEFT:
            if self.error:
                self.error = None
                clear = True
            self.selected = (self.selected - 1) % len(self.choices)

        ctx.redraw(clear)

    def _format_choices(self, selected: bool) -> str:
        return " / ".join(
            "{style}{c}{reset}".format(
                style=(util.UNDERLINE if i == self.selected else "")
                + (
                    (Fore.CYAN + Style.BRIGHT)
                    if selected and i == self.selected
                    else ""
                ),
                c=c,
                reset=Style.RESET_ALL,
            )
            for i, c in enumerate(self.choices)
        )

    def __format__(self, spec: str) -> str:
        selected = spec.split(",")[1] == ">"
        return "{color}{caret} {err}{prompt}: {reset}{choices}{reset} ".format(
            color=Fore.CYAN + Style.BRIGHT,
            caret=">" if selected else (" " + Style.RESET_ALL),
            err=self._format_error(selected),
            prompt=self.prompt,
            choices=self._format_choices(selected),
            reset=Style.RESET_ALL,
        )


class TextField(FormField):
    def __init__(
        self, id: str, prompt: str, rules: validation.TextRules = validation.TextRules()
    ) -> None:
        super().__init__(id)
        self.value = ""
        self.prompt = prompt
        self.rules = rules

    def select(self, ctx: "context.MenuContext") -> None:
        # we don't need to do anything here
        pass

    def on_key(self, key: str, ctx: "context.MenuContext") -> None:
        clear = False
        if len(key) == 1:
            if self.error:
                self.error = None
                clear = True

            # check for backspace
            if key == util.BACKSPACE:
                self.value = self.value[:-1]
            else:
                self.value += key

        ctx.redraw(clear)

    def validate(self) -> bool:
        valid, self.error = self.rules.validate(self.value)
        return valid

    def _format_output(self, spec: str, value: str) -> str:
        selected = spec.split(",")[1] == ">"
        return "{color}{caret} {err}{prompt}: {reset}{value}{cursor}{reset} ".format(
            color=Fore.CYAN + Style.BRIGHT,
            caret=">" if selected else (" " + Style.RESET_ALL),
            err=self._format_error(selected),
            prompt=self.prompt,
            value=value,
            cursor=util.UNDERLINE + (" " if selected else ""),
            reset=Style.RESET_ALL,
        )

    def __format__(self, spec: str) -> str:
        return self._format_output(spec, self.value)


class NumericField(TextField):
    rules: validation.NumericRules  # type: ignore

    def __init__(
        self,
        id: str,
        prompt: str,
        rules: validation.NumericRules = validation.NumericRules(),
    ) -> None:
        super().__init__(id, prompt)
        self.rules = rules  # type: ignore

    def on_key(self, key: str, ctx: "context.MenuContext") -> None:
        clear = False

        if len(key) == 1:
            if self.error:
                self.error = None
                clear = True

            if key == util.BACKSPACE:
                self.value = self.value[:-1]
            elif key.isdigit() or key == ".":
                self.value += key
            else:
                print("Invalid key:", key)

        ctx.redraw(clear)

    def validate(self) -> bool:
        valid, self.error = self.rules.validate(self.value)
        return valid

    def __format__(self, spec: str) -> str:
        return self._format_output(spec, str(self.value))


class PasswordField(TextField):
    def __format__(self, spec: str) -> str:
        return self._format_output(spec, "*" * len(self.value))


FormField.Select = SelectField
FormField.Text = TextField
FormField.Numeric = NumericField
FormField.Password = PasswordField
