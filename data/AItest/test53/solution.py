
def same_chars(s0: str, s1: str) -> bool:
    """
    Check if two words have the same characters.
    >>> same_chars('eabcdzzzz', 'dddzzzzzzzddeddabc')
    True
    >>> same_chars('abcd', 'dddddddabc')
    True
    >>> same_chars('dddddddabc', 'abcd')
    True
    >>> same_chars('eabcd', 'dddddddabc')
    False
    >>> same_chars('abcd', 'dddddddabce')
    False
    >>> same_chars('eabcdzzzz', 'dddzzzzzzzddddabc')
    False
    """
    return set(s0) == set(s1)

# test cases to validate the solution

assert(same_chars('eabcdzzzz', 'dddzzzzzzzddeddabc') == True)
assert(same_chars('abcd', 'dddddddabc') == True)
assert(same_chars('dddddddabc', 'abcd') == True)
assert(same_chars('eabcd', 'dddddddabc') == False)
assert(same_chars('abcd', 'dddddddabce') == False)
assert(same_chars('eabcdzzzz', 'dddzzzzzzzddddabc') == False)
