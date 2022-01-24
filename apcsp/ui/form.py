from abc import ABCMeta, abstractmethod
from inspect import getfullargspec
from typing import TYPE_CHECKING, Any, Callable, List, Tuple, Type

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

    def __init__(self, id: str) -> None:
        self.id = id
        self.error = None

    def _format_error(self, selected: bool) -> str:
        return (
            (Fore.RED + Style.BRIGHT + "! " + self.error + " " + Style.RESET_ALL)
            if self.error
            else ""
        ) + ((Fore.CYAN + Style.BRIGHT) if selected else "")

    def validate(self, ctx: "context.MenuContext") -> bool:
        return True

    Select: "Type[SelectField]"
    Text: "Type[TextField]"
    Numeric: "Type[NumericField]"
    Password: "Type[PasswordField]"


class SelectField(FormField):
    def __init__(
        self,
        id: str,
        prompt: str,
        choices: List[str],
        *,
        selected: int = 0,
    ) -> None:
        super().__init__(id)
        self.prompt = prompt
        self.choices = choices
        self.selected = selected

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
        self,
        id: str,
        prompt: str,
        *,
        rules: validation.TextRules | None = None,
        validator: "Callable[[str], Tuple[bool, str | None]] | None" = None,
        context_validator: "Callable[[str, context.MenuContext], Tuple[bool, str | None]] | None" = None,
        initial_value: str | None = "",
    ) -> None:
        if rules is not None and (
            validator is not None or context_validator is not None
        ):
            raise ValueError("Cannot specify both rules and a validator")
        if validator is not None and context_validator is not None:
            raise ValueError("Cannot specify both context_validator and validator")

        super().__init__(id)
        self.value = initial_value or ""
        self.prompt = prompt
        self.rules = rules or validation.TextRules()
        self.validator = validator
        self.context_validator = context_validator

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

    def validate(self, ctx: "context.MenuContext") -> bool:
        if self.validator is not None:
            valid, self.error = self.validator(self.value)
            return valid
        elif self.context_validator is not None:
            valid, self.error = self.context_validator(self.value, ctx)
            return valid
        elif self.rules is not None:
            valid, self.error = self.rules.validate(self.value)
        else:
            valid = True
            self.error = None
        return valid

    # def _format_output(self, spec: str, value: str) -> str:

    def __format__(self, spec: str) -> str:
        selected = spec.split(",")[1] == ">"
        return "{color}{caret} {err}{prompt}: {reset}{value}{cursor}{reset}    ".format(
            color=Fore.CYAN + Style.BRIGHT,
            caret=">" if selected else (" " + Style.RESET_ALL),
            err=self._format_error(selected),
            prompt=self.prompt,
            value=str(self.value),
            cursor=util.UNDERLINE + (" " if selected else ""),
            reset=Style.RESET_ALL,
        )


class NumericField(TextField):
    rules: validation.NumericRules  # type: ignore

    def __init__(
        self,
        id: str,
        prompt: str,
        *,
        rules: validation.NumericRules | None = None,
        validator: Callable[[str], Tuple[bool, str]] | None = None,
        context_validator: "Callable[[str, context.MenuContext], Tuple[bool, str]] | None" = None,
        initial_value: str | None = "",
    ) -> None:
        super().__init__(
            id,
            prompt,
            rules=rules,  # type: ignore
            validator=validator,
            context_validator=context_validator,
            initial_value=initial_value,
        )
        self.rules = rules or validation.NumericRules()  # type: ignore

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


class PasswordField(TextField):
    def __format__(self, spec: str) -> str:
        original_value = self.value
        self.value = "*" * len(self.value)
        output = super().__format__(spec)
        self.value = original_value
        return output


FormField.Select = SelectField
FormField.Text = TextField
FormField.Numeric = NumericField
FormField.Password = PasswordField
