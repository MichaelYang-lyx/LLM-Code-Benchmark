
def pluck(arr):
    smallest_even = None
    smallest_index = -1

    for index, val in enumerate(arr):
        if val % 2 == 0: # If val is even
            if smallest_even is None:
                smallest_even = val
                smallest_index = index
            elif val < smallest_even:
                smallest_even = val
                smallest_index = index
                
    if smallest_even is not None:
        return [smallest_even, smallest_index]
    else:
        return []
