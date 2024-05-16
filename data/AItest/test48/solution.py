
def is_palindrome(text: str):
    """
    Checks if given string is a palindrome
    >>> is_palindrome('')
    True
    >>> is_palindrome('aba')
    True
    >>> is_palindrome('aaaaa')
    True
    >>> is_palindrome('zbcd')
    False
    """
    # convert to lower case, remove non-alpha characters
    text = ''.join(char for char in text if char.isalpha()).lower()
    
    # check if text is the same when reversed
    return text == text[::-1]
