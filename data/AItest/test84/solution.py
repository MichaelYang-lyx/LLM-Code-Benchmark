
def add(lst):
    """Given a non-empty list of integers lst. add the even elements that are at odd indices..

    Args:
        lst: A non-empty list of integers

    Returns:
        int: The sum of even elements at odd indices

    Examples:
        add([4, 2, 6, 7]) ==> 2 
    """
    total = 0
    for i in range(1, len(lst), 2):
        if lst[i] % 2 == 0:
            total += lst[i]
    return total
