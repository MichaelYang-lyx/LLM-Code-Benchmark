
def circular_shift(x, shift):
    """Circular shift the digits of the integer x, shift the digits right by shift
    and return the result as a string.
    If shift > number of digits, return digits reversed.
    """
    string_x = str(x)
    length_x = len(string_x)
    
    if shift > length_x:
        return string_x[::-1] 
    else:
        shift %= length_x
        return string_x[-shift:] + string_x[:-shift]

print(circular_shift(12, 1))  # Outputs: "21"
print(circular_shift(12, 2))  # Outputs: "12"
