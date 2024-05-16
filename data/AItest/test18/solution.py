
def count_distinct_characters(string: str) -> int:
    """ Given a string, find out how many distinct characters (regardless of case) does it consist of
    >>> count_distinct_characters('xyzXYZ')
    3
    >>> count_distinct_characters('Jerry')
    4
    """
    string = string.lower()  # Convert the string to lowercase to ignore case
    distinct_chars = set(string)  # Use a set to store distinct characters
    return len(distinct_chars)  # Return the number of distinct characters
