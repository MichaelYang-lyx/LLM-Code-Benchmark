
def minSubArraySum(nums):
    min_sum = float('inf')
    current_sum = 0
    for num in nums:
        current_sum = min(num, current_sum + num)
        min_sum = min(min_sum, current_sum)
    return min_sum

print(minSubArraySum([2, 3, 4, 1, 2, 4]))  # Output: 1
print(minSubArraySum([-1, -2, -3]))  # Output: -6
