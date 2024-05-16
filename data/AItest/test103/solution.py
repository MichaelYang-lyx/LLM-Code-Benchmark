
def unique_digits(x):
    result = []
    for num in x:
        if all(int(digit) % 2 != 0 for digit in str(num)):
            result.append(num)
    return sorted(result)
