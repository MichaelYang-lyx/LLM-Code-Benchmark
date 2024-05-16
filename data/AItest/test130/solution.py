
def digits(n):
    product = 1
    for digit in str(n):
        if int(digit) % 2 != 0:
            product *= int(digit)
    return product

# Test cases
print(digits(1))   # Output: 1
print(digits(4))   # Output: 0
print(digits(235)) # Output: 15
