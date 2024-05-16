
def flip_case(string: str) -> str:
    """ For a given string, flip lowercase characters to uppercase and uppercase to lowercase.
    >>> flip_case('Hello')
    'hELLO'
    """
    flipped_string = ''
    for char in string:
        if char.islower():
            flipped_string += char.upper()
        elif char.isupper():
            flipped_string += char.lower()
        else:
            flipped_string += char
    return flipped_string
