
def sorted_list_sum(lst):
    # We filter only the strings with even length
    lst = [i for i in lst if len(i) % 2 == 0]
    
    # Then, we sort the list based on word length,
    # In case of equal lengths, we sort them in alphabetic order.
    lst.sort(key=lambda x: (len(x), x))

    return lst
