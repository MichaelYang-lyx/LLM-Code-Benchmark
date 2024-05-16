
from typing import List, Optional


def longest(strings: List[str]) -> Optional[str]:
    """ Out of list of strings, return the longest one. Return the first one in case of multiple
    strings of the same length. Return None in case the input list is empty.
    >>> longest([])
    
    >>> longest(['a', 'b', 'c'])
    'a'
    >>> longest(['a', 'bb', 'ccc'])
    'ccc'
    """
    if not strings:
        return None
    longest_str = strings[0]
    for s in strings:
        if len(s) > len(longest_str):
            longest_str = s
        elif len(s) == len(longest_str) and s != longest_str:
            longest_str = s
    return longest_str
