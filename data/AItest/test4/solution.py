
from typing import List

def separate_paren_groups(paren_string: str) -> List[str]:
    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced and nested within each other.
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    """
    cleaned_string = paren_string.replace(" ", "")
    stack = []
    result = []
    start = 0
    for i, ch in enumerate(cleaned_string):
        if ch == '(':
            if not stack:
                start = i
            stack.append(ch)
        elif ch == ')':
            stack.pop()
            if not stack:
                result.append(cleaned_string[start:i+1])
    return result
