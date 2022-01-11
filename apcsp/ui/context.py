from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from . import menu


class MenuContext(object):
    def __init__(
        self,
        *,
        context: "MenuContext | None" = None,
        parent: "menu.Menu | None" = None,
        data: Dict[str, Any] = None
    ):
        self.context = context
        self.parent = parent
        self.data = data or {}
