
import math

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n > 2 and n % 2 == 0:
        return False
    max_divisor = math.floor(math.sqrt(n))
    for d in range(3, max_divisor + 1, 2):
        if n % d == 0:
            return False
    return True

def prime_length(string):
    length = len(string)
    return is_prime(length)

# Test cases
print(prime_length('Hello'))  # Output: True
print(prime_length('abcdcba'))  # Output: True
print(prime_length('kittens'))  # Output: True
print(prime_length('orange'))  # Output: False
