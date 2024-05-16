
def strange_sort_list(lst):
    sorted_lst = []
    lst.sort()
    while len(lst) > 0:
        sorted_lst.append(lst.pop(0))
        if len(lst) > 0:
            sorted_lst.append(lst.pop(-1))
    return sorted_lst
