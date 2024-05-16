
def double_the_difference(lst):
    """
    Given a list of numbers, return the sum of squares of the numbers
    in the list that are odd. Ignore numbers that are negative or not integers.
    """
    return sum(x**2 for x in lst if isinstance(x, int) and x > 0 and x % 2 != 0)
