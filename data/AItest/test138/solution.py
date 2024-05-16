
def factorial(n):
    """Helper function to calculate factorial of n"""
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def special_factorial(n):
    """The Brazilian factorial is defined as:
    brazilian_factorial(n) = n! * (n-1)! * (n-2)! * ... * 1!
    where n > 0

    For example:
    >>> special_factorial(4)
    288

    The function will receive an integer as input and should return the special
    factorial of this integer.
    """
    result = 1
    for i in range(n, 0, -1):
        result *= factorial(i)
    return result

print(special_factorial(4))  # Output: 288
