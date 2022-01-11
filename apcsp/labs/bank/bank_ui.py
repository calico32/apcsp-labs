from apcsp.ui import Button, Exit, Menu, MenuContext, Submenu, Title

main_menu = Menu(
    Title(""),
    Submenu(
        "Submenu",
        Menu(
            Title("Submenu"),
            Submenu(
                "Subsubmenu",
                Menu(
                    Title("Subsubmenu"),
                    Exit(),
                ),
            ),
        ),
    ),
    Button("Exit", type="_exit"),
)


def ui_main(bank: Bank):  # type: ignore
    context = MenuContext()
    main_menu.run(context)
