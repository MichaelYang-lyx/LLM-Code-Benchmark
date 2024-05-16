
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
    text = text.lower()  # Convert the text to lowercase for case-insensitive comparison
    text = ''.join(e for e in text if e.isalnum())  # Remove any non-alphanumeric characters

    return text == text[::-1]  # Check if the text is equal to its reverse
