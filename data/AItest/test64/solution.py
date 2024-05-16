
def circular_shift(x, shift):
    x_str = str(x)
    length = len(x_str)
    shift = shift % length  # Ensure shift is within the length of the number
    
    if shift == 0:
        return x_str
    else:
        shifted = x_str[-shift:] + x_str[:-shift]
        return shifted
