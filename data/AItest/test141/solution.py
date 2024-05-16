
def sum_squares(lst):
    """"
    This function will take a list of integers. For all entries in the list, the function shall square the integer entry if its index is a 
    multiple of 3 and will cube the integer entry if its index is a multiple of 4 and not a multiple of 3. The function will not 
    change the entries in the list whose indexes are not a multiple of 3 or 4. The function shall then return the sum of all entries. 
    """
    total_sum = 0
    for i in range(len(lst)):
        if i % 3 == 0:  # We check if index i is a multiple of 3
            total_sum += lst[i]**2
        elif i % 4 == 0:  # We check if index i is a multiple of 4 but not a multiple of 3
            total_sum += lst[i]**3
        else:  # for other indexes, we don't change the integer
            total_sum += lst[i]
    return total_sum

# Test cases:
print(sum_squares([1,2,3]))  # Expected output: 6
print(sum_squares([]))  # Expected output: 0
print(sum_squares([-1,-5,2,-1,-5]))  # Expected output: -126
