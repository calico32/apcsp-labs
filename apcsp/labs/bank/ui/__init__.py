from ..bank import Bank, BankState
from . import login, money, profile, register
from .util import MenuOption, menu

unauth_menu = [
    MenuOption("", "Login", login.login),
    MenuOption("", "Register", register.register),
    MenuOption("", "Exit", lambda _: "_exit"),
]

auth_menu = [
    MenuOption("", "Deposit", money.deposit),
    MenuOption("", "Withdraw", money.withdraw),
    MenuOption("", "Transfer", money.transfer),
    MenuOption("", "View Transactions", money.view_transactions),
    MenuOption("Accounts", "Open new account", register.open_account),
    MenuOption("", "Close account", register.close_account),
    MenuOption("User", "Change name", profile.change_name),
    MenuOption("", "Change password", profile.change_password),
    MenuOption("", "Change PIN", profile.change_pin),
    MenuOption("", "Delete user account", profile.delete_user_account),
    MenuOption("Logout", "Logout", login.logout),
]


def ui_main(bank: Bank) -> None:
    state = BankState(bank)
    while True:
        if state.user:
            ret = menu(state, auth_menu)
        else:
            ret = menu(state, unauth_menu)
        if isinstance(ret, tuple):
            val = ret[2]
            if val == "_exit":
                break
