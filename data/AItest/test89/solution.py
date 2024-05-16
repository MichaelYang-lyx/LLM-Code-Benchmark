
def next_smallest(lst):
    if len(lst) < 2:
        return None
    sorted_lst = sorted(set(lst))
    if len(sorted_lst) < 2:
        return None
    return sorted_lst[1]
