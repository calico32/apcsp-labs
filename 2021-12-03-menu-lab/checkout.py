from datetime import datetime
from typing import List

from _util import Item, widths

SALES_TAX = 0.06825


def checkout(menu: List[Item]) -> None:
    subtotal = "{:.2f}".format(
        sum(item.subtotal for item in menu) / 100)
    tax = f"{SALES_TAX * 100:.3f}%"
    total = "{:.2f}".format(
        sum(item.subtotal for item in menu) * (1 + SALES_TAX) / 100)

    item_width = widths(menu)[1]
    quantity_width = max(len(str(item.count)) for item in menu) + 1
    last_col_width = max(
        max(len(str(item.subtotal)) for item in menu),
        len("Subtotal"),
        len(subtotal),
        len(total),
    )

    columns = f'| {{:>{quantity_width}}} {{:<{item_width}}} | {{:>{last_col_width}}} |'
    two_columns = f'| {{:<{quantity_width + 1 + item_width}}} | {{:>{last_col_width}}} |'
    single_column_width = quantity_width + 1 + item_width + 3 + last_col_width
    single_column = f'| {{:<{single_column_width}}} |'
    separator = f'+-{"-" * quantity_width}-{"-" * item_width}-+-{"-" * last_col_width}-+'

    column_names = two_columns.format('Item', 'Subtotal')

    print()
    print(separator)
    print(single_column.format('Copilot Cafe'.center(single_column_width)))
    print(single_column.format('*-*-*-*-*-*-*-*').center(single_column_width))
    print(two_columns.format(datetime.now().strftime('%a %m/%d/%y %I:%M:%S %p'), ''))
    print(column_names)
    print(separator)

    for item in filter(lambda item: item.count > 0, menu):
        print(columns.format(f'{item.count}×',
              item.name, item.subtotal_formatted))

    print(separator)
    print(two_columns.format('Subtotal', subtotal))
    print(two_columns.format('Sales Tax', tax))
    print(two_columns.format('Total', total))
    print(separator)

    exit()
