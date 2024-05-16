
def make_a_pile(n):
    pile = [n]
    for i in range(1, n):
        if n % 2 == 0:
            pile.append(n + 2*i)
        else:
            pile.append(n + 2*i + 1)
    return pile
