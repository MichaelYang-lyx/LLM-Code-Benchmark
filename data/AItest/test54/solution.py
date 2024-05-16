
def fib(n: int):
    """Return n-th Fibonacci number."""
    if n <= 0:
        raise ValueError('Input should be a positive integer.')
    elif n in [1, 2]:
        return n-1 if n==1 else 1
    else:
        return fib(n - 1) + fib(n - 2)

# Testing
print(fib(10))  # Output: 55
print(fib(1))   # Output: 0
print(fib(8))   # Output: 21
