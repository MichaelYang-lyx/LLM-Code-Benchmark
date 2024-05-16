
def compare_one(a, b):
    """
    Create a function that takes integers, floats, or strings representing
    real numbers, and returns the larger variable in its given variable type.
    Return None if the values are equal.
    Note: If a real number is represented as a string, the floating point might be . or ,
    """

    # First, we need to ensure that the values are numerical
    # If value is string, we convert to float
    try:
        if type(a) is str:
            a = float(a.replace(',', '.'))
        if type(b) is str:
            b = float(b.replace(',', '.'))
    except ValueError:
        return "Error: Both inputs need to be numbers or strings representing numbers."

    # Now, we can break down scenarios:
    # If two values are equal, return None
    if a == b:
        return None

    # If b is greater, return b
    if a < b:
        return b

    # If none of the above, then a must be greater
    return a
