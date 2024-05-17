def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def prime_fib(n: int):
    def fibonacci(n):
        fibs = [0, 1]
        for i in range(2, n+1):
            fibs.append(fibs[-1] + fibs[-2])
        return fibs[n]

    count = 0
    num = 1
    while count < n:
        fib_num = fibonacci(num)
        if is_prime(fib_num):
            count += 1
        num += 1

    return fib_num