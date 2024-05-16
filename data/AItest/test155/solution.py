
def int_to_mini_roman(number):
    """
    Given a positive integer, obtain its roman numeral equivalent as a string,
    and return it in lowercase.
    Restrictions: 1 <= num <= 1000

    Examples:
    >>> int_to_mini_roman(19) == 'xix'
    >>> int_to_mini_roman(152) == 'clii'
    >>> int_to_mini_roman(426) == 'cdxxvi'
    """
    value_map = {1: 'i', 4: 'iv', 5: 'v', 9: 'ix', 10: 'x', 40: 'xl', 
                50: 'l', 90: 'xc', 100: 'c', 400: 'cd', 500: 'd', 900: 'cm', 1000: 'm'}

    if number in value_map.keys():
        return value_map[number]
    
    roman = ''
    for i in sorted(value_map.keys(),reverse=True):
        while number >= i:
            roman += value_map[i]
            number -= i
    return roman

print(int_to_mini_roman(19)) # should return 'xix'
print(int_to_mini_roman(152)) # should return 'clii'
print(int_to_mini_roman(426)) # should return 'cdxxvi'
