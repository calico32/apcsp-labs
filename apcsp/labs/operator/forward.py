# input number of hours, minutes, and seconds
hours = int(input("Enter the number of hours: "))
minutes = int(input("Enter the number of minutes: "))
seconds = int(input("Enter the number of seconds: "))

# input output format: hours, minutes, or seconds
format = input("Enter the format you want to output (hours, minutes, seconds): ")

if format == "hours":
    result = hours + (minutes / 60) + (seconds / 3600)
elif format == "minutes":
    result = hours * 60 + minutes + (seconds / 60)
elif format == "seconds":
    result = hours * 3600 + minutes * 60 + seconds
else:
    print("Invalid format")
    exit()

print(f"{hours}h{minutes}m{seconds}s is equal to {result} seconds")


# thank you copilot
