
def change_base(x: int, base: int) -> str:
    """Change numerical base of the input number x to base.
    Returns a string representation after the conversion.
    Base numbers are less than 10.
    """

    if x == 0:
        return '0'
        
    digits = []

    while x:
        digits.append(str(x % base))
        x //= base

    digits.reverse()   # to get the right order
    return ''.join(digits)
