
def multiply(a, b):
    """Complete the function that takes two integers and returns 
    the product of their unit digits.
    Assume the input is always valid.
    Examples:
    multiply(148, 412) should return 16.
    multiply(19, 28) should return 72.
    multiply(2020, 1851) should return 0.
    multiply(14,-15) should return 20.
    """

    # Handle end cases with both positive and negative numbers
    a_unit = abs(a) % 10
    b_unit = abs(b) % 10

    return a_unit * b_unit

print(multiply(148, 412))  # 16
print(multiply(19, 28))  # 72
print(multiply(2020, 1851))  # 0
print(multiply(14, -15))  # 20
