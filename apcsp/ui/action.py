from inspect import getfullargspec
from typing import Any, Callable, Literal

from apcsp.ui import context, obj

ActionType = Literal["_exit", "_interrupt"]


class MenuAction(obj.HiddenObject):
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

    def execute(self, ctx: context.MenuContext) -> None:
        if self.run is None and self.type is None:
            print("WARNING: MenuAction has no action")

        if self.run is not None:
            spec = getfullargspec(self.run)
            if len(spec.args) == 0:
                self.run()
            elif len(spec.args) == 1:
                self.run(ctx)
            else:
                raise ValueError("MenuAction run function must take 0 or 1 argument")

        if self.type in ("_exit", "_interrupt"):
            ctx.exit()  # type: ignore # TODO
