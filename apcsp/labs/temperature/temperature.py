# convert f to c
def f_to_c(f: float):
    c = (f - 32) * 5 / 9
    return c


# convert c to f
def c_to_f(c: float):
    f = c * 9 / 5 + 32
    return f


if __name__ == "__main__":
    source: str = ""
    while not source:
        source = input("Enter source temperature (e.g. 32f, 16.3C): ").lower()

    try:
        if source.endswith("f"):
            value = float(source[:-1])
            source = f"{value}°F"
            result = f"{round(f_to_c(value), 2)}°C"
        elif source.endswith("c"):
            value = float(source[:-1])
            source = f"{value}°C"
            result = f"{round(c_to_f(value), 2)}°F"
        else:
            print("Invalid unit")
            exit()
    except ValueError:
        print("Invalid number")
        exit()

    print(f"{source} is equal to {result}")
