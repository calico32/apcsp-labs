input_seconds = int(input("Enter seconds: "))

minutes = input_seconds // 60
seconds = input_seconds % 60

hours = minutes // 60
minutes %= 60

print(f'{input_seconds} seconds is equal to {hours} hours, {minutes} minutes, and {seconds} seconds')
