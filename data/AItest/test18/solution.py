
def count_distinct_characters(string: str) -> int:
    """ Given a string, find out how many distinct characters (regardless of case) does it consist of
    >>> count_distinct_characters('xyzXYZ')
    3
    >>> count_distinct_characters('Jerry')
    4
    """
    # Converting the string to lower case to handle case sensitivity
    string = string.lower()
    # Using set data type to eliminate duplicates and count the distinct characters
    return len(set(string))
