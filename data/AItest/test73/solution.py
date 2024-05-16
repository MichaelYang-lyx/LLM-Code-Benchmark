
def total_match(lst1, lst2):
    '''
    Write a function that accepts two lists of strings and returns the list that has 
    total number of chars in the all strings of the list less than the other list.

    if the two lists have the same number of chars, return the first list.

    Examples
    total_match([], []) --> []
    total_match(['hi', 'admin'], ['hI', 'Hi']) --> ['hI', 'Hi']
    total_match(['hi', 'admin'], ['hi', 'hi', 'admin', 'project']) --> ['hi', 'admin']
    total_match(['hi', 'admin'], ['hI', 'hi', 'hi']) --> ['hI', 'hi', 'hi']
    total_match(['4'], ['1', '2', '3', '4', '5']) --> ['4']
    '''
    # Here we sum up the lengths of all the strings within each list
    length_lst1 = sum(len(s) for s in lst1)
    length_lst2 = sum(len(s) for s in lst2)

    # Return the list which has less total number of characters, or the first list if they're equal
    if length_lst1 <= length_lst2:
        return lst1
    else:
        return lst2
