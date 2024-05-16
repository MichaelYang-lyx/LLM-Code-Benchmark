
from math import sqrt

def largest_divisor(n: int) -> int:
    """ For a given number n, find the largest number that divides n evenly, smaller than n
    >>> largest_divisor(15)
    5
    """
    largest = 1
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            largest = i
    return largest
