
def starts_one_ends(n):
    count = 0
    if n == 1:
        count = 1
    else:
        count = 2 * 9 * 10 ** (n-2)
    return count
