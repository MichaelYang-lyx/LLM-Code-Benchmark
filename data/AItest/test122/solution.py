
def get_odd_collatz(n):
    sequence = []
    while n != 1:
        if n % 2 != 0:
            sequence.append(n)
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    sequence.append(1)
    return sorted(sequence)
