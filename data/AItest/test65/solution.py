
def digitSum(s):
    """Task
    Write a function that takes a string as input and returns the sum of the upper characters only'
    ASCII codes.
    """
    return sum(ord(c) for c in s if c.isupper())
