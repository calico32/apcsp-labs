# units to convert to, greatest to least
units = [
    ('year', 365 * 24 * 60 * 60),
    ('day', 24 * 60 * 60),
    ('hour', 60 * 60),
    ('minute', 60),
    ('second', 1),
]


# join list of strings with commas
def comma_separated_and(list: list[str]) -> str:
    if len(list) == 0:
        return ''
    elif len(list) == 1:
        return list[0]
    elif len(list) == 2:
        return f'{list[0]} and {list[1]}'
    else:
        return f'{", ".join(list[:-1])}, and {list[-1]}'


# convert values to string
def format_units(values: list[int]) -> str:
    out: list[str] = []
    for index, (unit, _) in enumerate(units):
        if values[index] > 0:
            out.append(
                f'{values[index]} {unit}{"s" if values[index] > 1 else ""}')

    return comma_separated_and(out)


# convert seconds to units
def calculate_units(seconds: int) -> str:
    values: list[int] = []

    for (index, (unit, conversion)) in enumerate(units):
        values.append(seconds // conversion)
        seconds %= conversion

    return format_units(values)


if __name__ == '__main__':
    try:
        seconds = int(input("Enter seconds: "))
    except ValueError:
        print("Invalid input. Exiting.")
        exit(1)

    print(f'{seconds} seconds is equal to {calculate_units(seconds)}')
