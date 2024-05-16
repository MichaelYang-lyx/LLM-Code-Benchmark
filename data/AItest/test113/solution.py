
def minSubArraySum(nums):
    """
    Given an array of integers nums, find the minimum sum of any non-empty sub-array
    of nums.
    Example
    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
    minSubArraySum([-1, -2, -3]) == -6
    """
    min_sum = float('inf') # Start with the largest possible value
    current_sum = 0
    for num in nums:
        if current_sum > 0: 
            # Current_sum adds up, but it is larger than 0, so if it is added to num, it will only make the sum larger, so it is not added.
            current_sum = num
        else: 
            # Current_sum itself is negative, and adding it to num will only make the sum smaller, so continue to add
            current_sum += num
        min_sum = min(min_sum, current_sum)
    return min_sum
