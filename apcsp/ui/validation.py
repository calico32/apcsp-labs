from abc import ABCMeta, abstractmethod
from types import NoneType
from typing import Any, Literal, Set, Tuple


class ValidationRules(metaclass=ABCMeta):
    @abstractmethod
    def validate(self, value: str) -> Tuple[bool, str | None]:
        pass


class TextRules(ValidationRules):
    def __init__(
        self,
        *,
        required: bool = True,
        min_length: int | None = None,
        max_length: int | None = None,
        valid_chars: str | None = None,
        disallowed_chars: str | None = None,
    ) -> None:
        self.required = required
        self.min_length = min_length
        self.max_length = max_length
        if valid_chars is not None and disallowed_chars is not None:
            raise ValueError("Cannot specify both valid_chars and disallowed_chars")
        self.valid_chars = valid_chars
        self.disallowed_chars = disallowed_chars

    def validate(self, value: str) -> Tuple[bool, str | None]:
        if (value.strip() == "" or not value) and self.required:
            return False, "required"

        if self.min_length is not None and len(value) < self.min_length:
            return False, f"too short (min: {self.min_length})"

        if self.max_length is not None and len(value) > self.max_length:
            return False, f"too long (max: {self.max_length})"

        invalid: Set[str] = set()

        if self.valid_chars is not None:
            for c in value:
                if c not in self.valid_chars:
                    invalid.add(c)
            if invalid:
                return False, f"invalid characters: {invalid}"

        if self.disallowed_chars is not None:
            for c in value:
                if c in self.disallowed_chars:
                    invalid.add(c)
            if invalid:
                return False, f"disallowed characters: {invalid}"

        return True, None


class NumericRules:
    def __init__(self, *, required: bool = True):
        self.required = required

    def validate(self, value: str) -> Tuple[bool, str | None]:
        if str(value).strip() == "" and self.required:
            return False, "required"

        return True, None


class IntRules(NumericRules):
    def __init__(
        self, *, required: bool = True, min: int | None = None, max: int | None = None
    ) -> None:
        super().__init__(required=required)
        self.min = min
        self.max = max

    def validate(self, value: str) -> Tuple[bool, str | None]:
        if str(value).strip() == "" and self.required:
            return False, "required"

        try:
            f = int(value)
        except ValueError:
            return False, "invalid integer"

        if self.min is not None and f < self.min:
            return False, f"below min ({self.min})"
        if self.max is not None and f > self.max:
            return False, f"above max ({self.max})"
        return True, None


class FloatRules(NumericRules):
    def __init__(
        self,
        *,
        required: bool = True,
        min: float | None = None,
        max: float | None = None,
    ) -> None:
        super().__init__(required=required)
        self.min = min
        self.max = max

    def validate(self, value: str) -> Tuple[bool, str | None]:
        if str(value).strip() == "" and self.required:
            return False, "required"

        try:
            f = float(value)
        except ValueError:
            return False, "not a number"

        if self.min is not None and f < self.min:
            return False, f"below min ({self.min})"
        if self.max is not None and f > self.max:
            return False, f"above max ({self.max})"
        return True, None
