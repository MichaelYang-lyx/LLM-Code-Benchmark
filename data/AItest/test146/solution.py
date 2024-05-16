
def get_max_triples(n):
    count = 0
    a = [i * i - i + 1 for i in range(1, n + 1)]
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if (a[i] + a[j] + a[k]) % 3 == 0:
                    count += 1
    return count
