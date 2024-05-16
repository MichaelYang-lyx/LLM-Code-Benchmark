
def fibfib(n: int):
    if n == 0:
        return 0
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        fibfib_n_minus_1 = 1
        fibfib_n_minus_2 = 0
        fibfib_n_minus_3 = 0
        result = 0
        for i in range(3, n + 1):
            result = fibfib_n_minus_1 + fibfib_n_minus_2 + fibfib_n_minus_3
            fibfib_n_minus_3 = fibfib_n_minus_2
            fibfib_n_minus_2 = fibfib_n_minus_1
            fibfib_n_minus_1 = result
        return result

# Test cases
print(fibfib(1)) # Output: 0
print(fibfib(5)) # Output: 4
print(fibfib(8)) # Output: 24
