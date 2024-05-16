
def int_to_mini_roman(number):
    roman_numerals = {
        1: 'i', 4: 'iv', 5: 'v', 9: 'ix', 10: 'x', 40: 'xl', 50: 'l',
        90: 'xc', 100: 'c', 400: 'cd', 500: 'd', 900: 'cm', 1000: 'm'
    }
    result = ''
    for value in sorted(roman_numerals.keys(), reverse=True):
        while number >= value:
            result += roman_numerals[value]
            number -= value
    return result.lower()
