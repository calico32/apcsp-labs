from apcsp.ui.action import MenuAction
from apcsp.ui.context import MenuContext
from apcsp.ui.menu import Menu
from apcsp.ui.obj import Category, Title
from apcsp.ui.selectable import Button, Selectable
from apcsp.ui.util import clear


def on_interrupt(context: MenuContext) -> None:
    clear()
    print("interrupted")
    exit(0)


main = Menu(
    Title("Example Menu"),
    Category("Category 1"),
    Button("Button 1"),
    Button("Button 2"),
    Category("Category 2"),
    Button("Button 3"),
    Button("Button 4"),
    Button("Exit", type="_exit"),
    MenuAction(type="_interrupt", run=on_interrupt),
)

main.run(MenuContext())
