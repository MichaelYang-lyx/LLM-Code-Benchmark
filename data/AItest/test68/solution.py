
def search(lst):
    from collections import Counter

    dict_count = Counter(lst)
    greatest = -1

    for num, cnt in dict_count.items():
        if num > greatest and cnt >= num:
            greatest = num
    
    return greatest
