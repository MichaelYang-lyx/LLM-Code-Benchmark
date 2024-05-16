
def f(n):
    def factorial(num):
        if num == 0 or num == 1:
            return 1
        else:
            return num * factorial(num-1)

    result = []
    for i in range(1, n+1):
        if i % 2 == 0:
            result.append(factorial(i))
        else:
            result.append(sum(range(1, i+1)))
    return result
