
import math

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def count_up_to(n):
    primes = []
    for i in range(2, n):
        if is_prime(i):
            primes.append(i)
    return primes
