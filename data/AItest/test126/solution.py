
import math

def intersection(interval1, interval2):
    def is_prime(n):
        """Test if n is a prime number."""
        if n < 2:
            return False
        for i in range(2, math.isqrt(n) + 1):
            if n % i == 0:
                return False
        return True

    interval = max(interval1[0], interval2[0]), min(interval1[1], interval2[1])
    if interval[0] <= interval[1] and is_prime(interval[1] - interval[0]):
        return "YES"
    return "NO"
