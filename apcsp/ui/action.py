from typing import Any, Callable, Literal

from . import obj

ActionType = Literal["_exit", "_interrupt"]


class MenuAction(obj.MenuObject):
    def __init__(
        self,
        *,
        key: str | None = None,
        run: Callable[..., Any] = lambda: None,
        type: ActionType | None = None,
    ):
        if key is None and run is None and type is None:
            raise ValueError("MenuAction must have at least one argument")

        self.key = key
        self.run = run
        self.type = type
