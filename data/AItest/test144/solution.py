
def order_by_points(nums):
    """
    Write a function which sorts the given list of integers
    in ascending order according to the sum of their digits.
    Note: if there are several items with similar sum of their digits,
    order them based on their index in the original list.

    For example:
    >>> order_by_points([1, 11, -1, -11, -12]) == [-1, -11, 1, -12, 11]
    >>> order_by_points([]) == []
    """
    # Your implementation here
    def sum_of_digits(n):
        return sum(int(digit) for digit in str(abs(n)))

    # Use the in-built Python Sorted function with a lambda function to 
    # compare the sum of the digits of the numbers in the list.
    sorted_nums = sorted(nums, key=lambda x: sum_of_digits(x))
    
    return sorted_nums
