
def choose_num(x, y):
    """This function takes two positive numbers x and y and returns the
    biggest even integer number that is in the range [x, y] inclusive. If 
    there's no such number, then the function should return -1.

    For example:
    choose_num(12, 15) = 14
    choose_num(13, 12) = -1
    """
    # Ensure x is smaller than y
    if x > y:
        x, y = y, x 

    # Iterates from y to x in reverse order
    for i in range(y, x - 1, -1):
        if i % 2 == 0:
            # Returns the first even number it encounters
            return i

    # If the loop completes without finding an even number, return -1
    return -1
    