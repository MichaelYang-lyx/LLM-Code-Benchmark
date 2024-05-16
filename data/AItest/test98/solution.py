
def closest_integer(value):
    num = float(value)
    if num % 1 < 0.5:
        return int(num)
    elif num > 0:
        return int(num) + 1
    else:
        return int(num) - 1

# Test cases
print(closest_integer("10"))  # Output: 10
print(closest_integer("15.3"))  # Output: 15
print(closest_integer("14.5"))  # Output: 15
print(closest_integer("-14.5"))  # Output: -15
