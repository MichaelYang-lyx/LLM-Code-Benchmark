
def tri(n):
    sequence = [0, 1, 1]
    for i in range(3, n + 1):
        next_number = sequence[i - 1] + sequence[i - 2] + sequence[i - 3]
        sequence.append(next_number)
    return sequence
