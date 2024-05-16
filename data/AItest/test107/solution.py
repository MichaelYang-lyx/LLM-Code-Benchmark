
def count_nums(arr):
    """
    Write a function count_nums which takes an array of integers and returns
    the number of elements which has a sum of digits > 0.
    If a number is negative, then its first signed digit will be negative:
    e.g. -123 has signed digits -1, 2, and 3.
    >>> count_nums([]) == 0
    >>> count_nums([-1, 11, -11]) == 1
    >>> count_nums([1, 1, 2]) == 3
    """

    count = 0

    for num in arr:
        # In case of negative numbers, the first digit should be -1 times its absolute value
        if num < 0:
            digit_sum = -1 * int(str(abs(num))[0])
            digit_sum += sum(int(digit) for digit in str(abs(num))[1:])

        else:
            digit_sum = sum(int(digit) for digit in str(num))

        # if the sum of digits > 0, increase the count
        if digit_sum > 0:
            count += 1
    
    return count
