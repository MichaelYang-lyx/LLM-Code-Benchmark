
import math

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

# Test cases
print(is_prime(6))    # Output: False
print(is_prime(101))  # Output: True
print(is_prime(11))   # Output: True
print(is_prime(13441))# Output: True
print(is_prime(61))   # Output: True
print(is_prime(4))    # Output: False
print(is_prime(1))    # Output: False
