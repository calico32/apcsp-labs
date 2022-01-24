from typing import TYPE_CHECKING, List

from apcsp.ui import action, form, obj, selectable, util
from colorama import Cursor  # type: ignore
from readchar import readkey  # type: ignore

if TYPE_CHECKING:
    from apcsp.ui import context


class Menu(object):
    def __init__(self, *objects: obj.MenuObject) -> None:
        if not any(isinstance(obj, selectable.Selectable) for obj in objects):
            raise ValueError(
                "objects must contain at least one selectable.selectable object"
            )
        self.objects = objects
        self.selected = 0
        while True:
            if isinstance(self.objects[self.selected], selectable.Selectable):
                break
            self.selected += 1

    @property
    def fields(self) -> List[form.FormField]:
        fields: List[form.FormField] = []
        for o in self.objects:
            if isinstance(o, form.FormField):
                fields.append(o)
        return fields

    def cursor_up(self) -> None:
        while True:
            self.selected = (self.selected - 1) % len(self.objects)
            if isinstance(self.objects[self.selected], selectable.Selectable):
                break

    def cursor_down(self) -> None:
        while True:
            self.selected = (self.selected + 1) % len(self.objects)
            if isinstance(self.objects[self.selected], selectable.Selectable):
                break

    def lines(self, ctx: "context.MenuContext") -> List[str]:
        parent = ctx.parent

        if parent:
            assert parent.menu, "Parent context has no menu"
            parent_lines = parent.menu.lines(parent)  # TODO
            parent_width = max(util.strlen(s) for s in [*parent_lines, ""]) + 1

        lines = []

        for index, option in enumerate(self.objects):
            if isinstance(option, obj.HiddenObject):
                continue

            line = ""

            spec = ""
            spec += str(self.selected) or "."
            spec += ","
            spec += ">" if self.selected == index else "."
            line += format(option, spec)

            lines.append(line)

        if parent is None:
            return lines

        for i in range(max(len(lines), len(parent_lines))):
            line = ""
            if i < len(parent_lines):
                line += util.pad_end(parent_lines[i], parent_width) + "| "
            else:
                line += "".ljust(parent_width) + "| "

            if i < len(lines):
                line += lines[i]
                lines[i] = line
            else:
                lines.append(line)

        return lines

    def print(self, ctx: "context.MenuContext", clear: bool = True) -> str:
        if ctx.menu != self:
            return ""

        if clear:
            util.clear()
        else:
            print(Cursor.POS(0, 0), end="")
        out = "\n".join(self.lines(ctx))
        print(out)
        print()
        return out

    def run(self, ctx: "context.MenuContext") -> None:
        if ctx.exit_next:
            return
        if ctx.menu != self:
            return

        self.print(ctx)
        while True:
            if ctx.exit_next:
                return

            key = readkey()
            if util.interrupted(key):
                for obj in self.objects:
                    if isinstance(obj, action.MenuAction):
                        if obj.type == "_interrupt":
                            obj.execute(ctx)
                            return
                return
            elif key == util.ARROW_UP:
                self.cursor_up()
                self.print(ctx)
            elif key == util.ARROW_DOWN:
                self.cursor_down()
                self.print(ctx)
            elif key == "\r":
                assert isinstance(
                    (opt := self.objects[self.selected]), selectable.Selectable
                )

                opt.select(ctx)

                self.print(ctx)
            else:
                for index, obj in enumerate(self.objects):
                    if isinstance(obj, action.MenuAction) and obj.key == key:
                        obj.run(ctx)

                    if index == self.selected and isinstance(obj, form.KeyReceiver):
                        obj.on_key(key, ctx)
