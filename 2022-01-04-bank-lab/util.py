import random
from typing import Dict, Literal

id_counters: Dict[str, int] = {}


def create_id(namespace: str) -> str:
    assert len(namespace) > 0, "Namespace cannot be empty"
    if namespace not in id_counters:
        id_counters[namespace] = -1
    id_counters[namespace] += 1
    return f"{namespace}{id_counters[namespace]}"


def sign(amount: float | int) -> str:
    """Returns a string representing the sign of the given amount."""
    if amount < 0:
        return "-"
    elif amount > 0:
        return "+"
    else:
        return ""


def format_amount(amount: int, include_sign: bool | Literal["negative"] = True) -> str:
    """Returns a string representing the given amount."""
    if include_sign == "negative":
        if amount < 0:
            sign_str = sign(amount)
        else:
            sign_str = ""
    else:
        sign_str = sign(amount) if include_sign else ""

    return f"{sign_str}${abs(amount) // 100:,}.{abs(amount) % 100:02}"
