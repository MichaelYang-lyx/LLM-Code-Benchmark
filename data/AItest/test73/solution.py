
def total_match(lst1, lst2):
    total_chars_lst1 = sum(len(word) for word in lst1)
    total_chars_lst2 = sum(len(word) for word in lst2)

    if total_chars_lst1 < total_chars_lst2:
        return lst1
    elif total_chars_lst2 < total_chars_lst1:
        return lst2
    else:
        return lst1
