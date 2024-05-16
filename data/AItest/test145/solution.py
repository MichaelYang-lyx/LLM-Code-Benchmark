
def specialFilter(nums):
    count = 0
    for num in nums:
        if num > 10 and str(num)[0] in ['1', '3', '5', '7', '9'] and str(num)[-1] in ['1', '3', '5', '7', '9']:
            count += 1
    return count

# Test cases
print(specialFilter([15, -73, 14, -15]))  # Output: 1
print(specialFilter([33, -2, -3, 45, 21, 109]))  # Output: 2
