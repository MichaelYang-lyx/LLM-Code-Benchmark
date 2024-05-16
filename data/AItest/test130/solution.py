
def digits(n):
    """Given a positive integer n, return the product of the odd digits.
    Return 0 if all digits are even.
    For example:
    digits(1)  == 1
    digits(4)  == 0
    digits(235) == 15
    """
    product = 1
    is_odd_exist = False

    while n > 0:
        digit = n % 10
        if digit % 2 != 0:  # check if the digit is odd
            is_odd_exist = True
            product *= digit
        n = int(n / 10)

    if is_odd_exist:
        return product
    else:
        return 0


print(digits(1))  # Expected output is 1
print(digits(4))  # Expected output is 0
print(digits(235))  # Expected output is 15
