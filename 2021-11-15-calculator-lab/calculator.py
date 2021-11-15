# get the first number
first_number = int(input("Enter the first number: "))
# get the second number
second_number = int(input("Enter the second number: "))
# get the operator
operator = input("Enter the operator: ")

if operator == "+":
    print(first_number + second_number)
elif operator == "-":
    print(first_number - second_number)
elif operator == "*":
    print(first_number * second_number)
elif operator == "/":
    # check for divide by zero
    if second_number == 0:
        print("Cannot divide by zero.")
    else:
        print(first_number / second_number)
else:
    print("Invalid operator.")
