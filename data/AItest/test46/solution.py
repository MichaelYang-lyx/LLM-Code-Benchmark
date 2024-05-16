
def fib4(n: int) -> int:
    if n == 0: 
        return 0
    elif n == 1: 
        return 0
    elif n == 2: 
        return 2
    elif n == 3: 
        return 0
    else: 
        a, b, c, d = 0, 0, 2, 0
        for _ in range(4, n+1):
            a, b, c, d = b, c, d, a+b+c+d
        return d

# Testing the function
print(fib4(5))  # should print 4
print(fib4(6))  # should print 8
print(fib4(7))  # should print 14
