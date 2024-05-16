
def starts_one_ends(n):
    """
    Given a positive integer n, return the count of the numbers of n-digit
    positive integers that start or end with 1.
    """
    if n == 0:
        return 0
    elif n == 1:
        return 2  # 1 and 1
    else:
        return (10 ** (n-1)) + (8 * 10 ** (n-2))
