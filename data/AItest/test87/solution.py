
def sort_array(array):
    sorted_array = array.copy()
    sum_first_last = array[0] + array[-1]
    
    if sum_first_last % 2 == 0:
        sorted_array.sort(reverse=True)
    else:
        sorted_array.sort()
    
    return sorted_array
