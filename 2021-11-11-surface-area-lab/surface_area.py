def area(s1: float, s2: float) -> float:
    return s1 * s2


def surface_area(s1: float, s2: float, s3: float) -> float:
    return 2 * (area(s1, s2) + area(s2, s3) + area(s1, s3))


if __name__ == "__main__":
    s1 = float(input("Enter side 1 length: "))
    s2 = float(input("Enter side 2 length: "))
    s3 = float(input("Enter side 3 length: "))
    print(f"Surface area: {surface_area(s1, s2, s3)} units")
