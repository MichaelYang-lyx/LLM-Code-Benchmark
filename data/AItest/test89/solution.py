
def next_smallest(lst):
    """
    You are given a list of integers.
    Write a function next_smallest() that returns the 2nd smallest element of the list.
    Return None if there is no such element.
    
    next_smallest([1, 2, 3, 4, 5]) == 2
    next_smallest([5, 1, 4, 3, 2]) == 2
    next_smallest([]) == None
    next_smallest([1, 1]) == None
    """
    
    # Duplicate original list and convert to a set to remove duplicates
    unique_lst = set(lst)

    # Check if there are less than 2 unique elements
    # If so, return None
    if len(unique_lst) < 2:
        return None

    # Sort the unique list
    sorted_lst = sorted(unique_lst)

    # The 2nd smallest element will be at index 1
    return sorted_lst[1]
