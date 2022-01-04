# units to convert to, least to greatest
units = [
    ("minute", 60),
    ("hour", 60),
    ("day", 24),
    ("year", 365),
]


# join list of strings with commas
def comma_separated_and(l: list[str]) -> str:
    if len(l) == 0:
        return ""
    elif len(l) == 1:
        return l[0]
    elif len(l) == 2:
        return f"{l[0]} and {l[1]}"
    else:
        return f'{", ".join(l[:-1])}, and {l[-1]}'


# convert values to string
def format_units(values: list[tuple[int, str]]) -> str:
    out: list[str] = []
    for count, name in values:
        out.append(f'{count} {name}{"s" if count != 1 else ""}')

    return comma_separated_and(out)


# convert seconds to units
def calculate_units(seconds: int) -> str:
    values: list[tuple[int, str]] = [(seconds, "second")]

    for name, conversion in units:
        current_count, current_name = values[0]
        next_count = current_count // conversion

        if next_count == 0:
            break

        values[0] = (current_count % conversion, current_name)
        values.insert(0, (next_count, name))

    return format_units(values)


if __name__ == "__main__":
    try:
        seconds = int(input("Enter seconds (int): "))
    except ValueError:
        print("Invalid input. Exiting.")
        exit(1)

    print(f"{seconds} seconds is equal to {calculate_units(seconds)}")
