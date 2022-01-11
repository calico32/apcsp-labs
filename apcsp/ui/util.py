import os
import re

ARROW_UP = "\x1b[A"
ARROW_DOWN = "\x1b[B"

# keypresses used for exiting current menu
def interrupted(key: str) -> bool:
    return key in ["q", "Q", "\x1b", "\x1b\x1b", "\x03", "\x04"]


# clear the screen
def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def strlen(s: str) -> int:
    return len(ansi_escape.sub("", s))


def pad_end(s: str, width: int) -> str:
    return s + " " * (width - strlen(s))
