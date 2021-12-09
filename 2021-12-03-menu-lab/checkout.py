from datetime import datetime
from random import choice
from string import ascii_uppercase, digits
from typing import Callable, List, Tuple

from _prompt import _error
from _util import CURRENCY, Item, widths

SALES_TAX = 0.06825


class _ColumnFormatter:
    w1: int
    w2: int
    w3: int
    c1w: int
    c2w: int

    def __init__(self, countw: int, itemw: int, lastcolw: int) -> None:
        self.w1 = countw
        self.w2 = itemw
        self.w3 = lastcolw

        self.c1w = countw + 1 + itemw + 3 + lastcolw
        self.c2w = countw + 1 + itemw

    def c1(self, a1) -> str:
        return f'| {{:<{self.c1w}}} |'.format(a1)

    def c2(self, a1, a2, separator=True) -> str:
        return f'| {{:<{self.c2w}}} | {{:>{self.w3}}} |'.format(a1, a2) if separator else \
               f'| {{:<{self.c2w}}}   {{:>{self.w3}}} |'.format(a1, a2)

    def c3(self, a1, a2, a3) -> str:
        return f'| {{:>{self.w1}}} {{:<{self.w2}}} | {{:>{self.w3}}} |'.format(a1, a2, a3)


def _formatter(w1: int, w2: int, w3: int) -> Tuple[_ColumnFormatter, Callable[..., None], Callable[..., None], Callable[..., None]]:
    fmt = _ColumnFormatter(w1, w2, w3)

    def c1(a1=''): print(fmt.c1(a1))
    def c2(a1='', a2=''): print(fmt.c2(a1, a2))
    def c3(a1='', a2='', a3=''): print(fmt.c3(a1, a2, a3))

    return fmt, c1, c2, c3


def random_order_id():
    return ''.join(choice(ascii_uppercase + digits) for _ in range(8))


def checkout(menu: List[Item]) -> None:
    if len(list(filter(lambda x: x.count > 0, menu))) == 0:
        _error('You must have at least one item in your order!')
        return

    subtotal = sum(item.subtotal for item in menu)

    subtotal_fmt = f"{subtotal / 100:.2f} {CURRENCY}"
    tax_fmt = f"{SALES_TAX * 100:.3f}%"
    total_fmt = f"{subtotal * (1 + SALES_TAX) / 100:.2f} {CURRENCY}"

    w1 = max(len(str(item.count)) for item in menu) + 1
    w2 = widths(menu)[1]
    w3 = max(
        max(len(str(item.subtotal)) for item in menu),
        len("Subtotal"),
        len(subtotal_fmt),
        len(total_fmt),
    )

    border = f'+-{"-" * w1}-{"-" * w2}---{"-" * w3}-+'
    separator = f'+-{"-" * w1}-{"-" * w2}-+-{"-" * w3}-+'

    fmt, c1, c2, c3 = _formatter(w1, w2, w3)

    print()
    print(border)
    c1('Copilot Cafe'.center(fmt.c1w))
    c1('*-*-*-*-*-*-*-*'.center(fmt.c1w))
    c1(datetime.now().strftime('%a %m/%d/%y %I:%M:%S %p').center(fmt.c1w))
    c1(f'Order ID: {random_order_id()}'.center(fmt.c1w))
    print(separator)
    c2('Item', 'Subtotal')
    print(separator)

    for item in filter(lambda item: item.count > 0, menu):
        c3(f'{item.count}×', item.name, item.subtotal_formatted)

    print(separator)
    c2('Subtotal'.rjust(fmt.c2w), subtotal_fmt)
    c2('Sales Tax'.rjust(fmt.c2w), tax_fmt)
    c2('Total'.rjust(fmt.c2w), total_fmt)
    print(separator)

    c1('Thank you for your order!'.center(fmt.c1w))
    c1('Please come again'.center(fmt.c1w))
    print(border)

    exit()
