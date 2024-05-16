
import math

def prime_fib(n: int):
    """prime_fib returns n-th number that is a Fibonacci number and it's also prime."""
    def is_prime(num: int):
        """Check if a number is a prime number."""
        if num == 1:
            return False
        if num == 2:
            return True
        if num > 2 and num % 2 == 0:
            return False

        sqrt_num = math.isqrt(num)
        for i in range(3, sqrt_num + 1, 2):
            if num % i == 0:
                return False
        return True

    def next_fib(a: int, b: int):
        """Generates the next Fibonacci number."""
        return a + b

    # Initialize Fibonacci sequence
    fib_seq = [0, 1]
    count_prime = 0
    i = 2
    while count_prime < n:
        fib_seq.append(next_fib(fib_seq[i-1], fib_seq[i-2]))
        if is_prime(fib_seq[-1]):
            count_prime += 1
        i += 1

    return fib_seq[-1]

print(prime_fib(1))   # outputs: 2
print(prime_fib(2))   # outputs: 3
print(prime_fib(3))   # outputs: 5
print(prime_fib(4))   # outputs: 13
print(prime_fib(5))   # outputs: 89
