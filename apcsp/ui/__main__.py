from apcsp.ui.action import MenuAction
from apcsp.ui.context import MenuContext
from apcsp.ui.form import FormField, NumericField, PasswordField, SelectField, TextField
from apcsp.ui.menu import Menu
from apcsp.ui.obj import Category, Empty, Text, Title
from apcsp.ui.selectable import Button, FormResult
from apcsp.ui.util import clear
from apcsp.ui.validation import IntRules, TextRules

"""
apcsp.ui
Example ui code
"""


def on_interrupt(ctx: MenuContext) -> None:
    print("interrupted")
    exit(0)


def submit(ctx: MenuContext, data: FormResult) -> None:
    clear()
    print("submit")
    for k, v in data.items():
        print(f"{k}: {v}")
    exit(0)


main = Menu(
    Title("Example Menu"),
    Category("Category 1"),
    Button("Button 1"),
    Text("  Lorem ipsum dolor sit amet, consectetur adipiscing elit. "),
    Button.Submenu(
        "Example Form",
        Menu(
            Title("Example Form"),
            Category("Field types"),
            FormField.Text("text1", "Enter text"),
            FormField.Numeric("num1", "Enter integer", rules=IntRules()),
            FormField.Password("pass1", "Enter password"),
            FormField.Select("select1", "Select", ["Foo", "Bar", "Baz"]),
            Category("Validation"),
            FormField.Text("text2", "Optional text", rules=TextRules(required=False)),
            FormField.Text("text3", "Min length", rules=TextRules(min_length=3)),
            FormField.Text("text4", "Max length", rules=TextRules(max_length=4)),
            FormField.Text(
                "text5",
                "Disallowed chars (!,*)",
                rules=TextRules(disallowed_chars="!*"),
            ),
            Text.Empty(),
            Button.Cancel(),
            Button.Submit(on_submit=submit),
        ),
    ),
    Category("Category 2"),
    Button("Button 3"),
    Button.Submenu(
        "Submenu 2",
        Menu(
            Title("Submenu"),
            Category("Category 2"),
            Button("Button 4"),
            Button.Submenu(
                "Subsubmenu 1",
                Menu(
                    Title("Subsubmenu"),
                    Category("Category 3"),
                    Button("Button 5"),
                    Category("Category 4"),
                    Button("Button 6"),
                    Button.Exit(),
                ),
            ),
            Button.Exit(),
        ),
    ),
    Button.Exit(),
    MenuAction(type="_interrupt", run=on_interrupt),
)

clear()
MenuContext(main).run()
