
def unique_digits(x):
    result = [num for num in x if all(digit not in str(num) for digit in '02468')]
    result.sort()
    return result
