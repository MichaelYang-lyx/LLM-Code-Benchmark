
def sort_array(array):
    # Create a new list that's a copy of the array
    new_array = array[:]

    # Return if the array is empty or contains only one element 
    if len(new_array) < 2:
        return new_array

    # check whether sum of first and last element is even
    if (new_array[0] + new_array[-1]) % 2 == 0:
        # if it's even, sort in descending order
        new_array.sort(reverse=True)
    else:
        # if it's odd, sort in ascending order
        new_array.sort()

    return new_array
