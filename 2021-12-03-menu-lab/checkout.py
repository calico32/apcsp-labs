from typing import List

from util import Item, widths

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

    single_columns = '| {:<' + str(quantity_width + item_width + 1) + \
        '} | {:>' + str(last_col_width) + '} |'
    columns = '| {:>' + str(quantity_width) + '} {:<' + \
        str(item_width) + '} | {:>' + str(last_col_width) + '} |'

    separator = '+-' + ('-' * quantity_width) + '-' + ('-' * item_width) + '-+-' + \
        ('-' * last_col_width) + '-+'

    column_names = single_columns.format('Item', 'Subtotal')

    print()
    print(separator)
    print(single_columns.format('Copilot Cafe™', ''))
    print(single_columns.format('', ''))
    print(column_names)
    print(separator)

    for item in filter(lambda item: item.count > 0, menu):
        print(columns.format(f'{item.count}×',
              item.name, item.subtotal_formatted))

    print(separator)
    print(single_columns.format('Subtotal', subtotal))
    print(single_columns.format('Sales Tax', tax))
    print(single_columns.format('Total', total))
    print(separator)

    exit()
