
def fruit_distribution(s, n):
    apples = int(s.split(' ')[0])
    oranges = int(s.split(' ')[3])
    mangoes = n - apples - oranges
    return mangoes
