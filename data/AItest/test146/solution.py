
def get_max_triples(n):
    count = [0] * 3
    res = 0
    for i in range(1, n+1):
        ai = i * i - i + 1
        res += count[(-ai % 3) % 3]
        count[ai % 3] += 1
    return res
