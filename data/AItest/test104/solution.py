
def by_length(arr):
    number_names = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    sorted_arr = sorted([x for x in arr if 1 <= x <= 9])
    reversed_arr = sorted_arr[::-1]
    result = [number_names[x] for x in reversed_arr]
    return result
