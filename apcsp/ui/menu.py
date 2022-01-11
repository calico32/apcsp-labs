from typing import TYPE_CHECKING, List

from readchar import readkey  # type: ignore

from . import action, obj, selectable, util

if TYPE_CHECKING:
    from . import context


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

    def lines(self, context: "context.MenuContext") -> List[str]:
        parent = context.parent

        if parent:
            parent_lines = parent.lines(context)  # TODO
            parent_width = max(util.strlen(s) for s in [*parent_lines, ""]) + 1

        lines = []

        for index, option in enumerate(self.objects):
            line = ""

            spec = ""
            spec += ">" if self.selected == index else " "
            if isinstance(option, (obj.Title, obj.Category, selectable.Button)):
                line += format(option)

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

    def print(self, context: "context.MenuContext") -> str:
        util.clear()
        return "\n".join(self.lines(context))

    def run(self, context: "context.MenuContext") -> None:
        self.print(context)
        while True:
            key = readkey()
            if util.interrupted(key):
                return
            elif key == util.ARROW_UP:
                self.cursor_up()
                self.print(context)
            elif key == util.ARROW_DOWN:
                self.cursor_down()
                self.print(context)
            elif key == "\r":
                assert isinstance(
                    (opt := self.objects[self.selected]), selectable.Selectable
                )

                opt.select(context)

                self.print(context)
            else:
                for obj in self.objects:
                    if isinstance(obj, action.MenuAction) and obj.key == key:
                        obj.run(context)
                        break
