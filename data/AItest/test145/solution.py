
def specialFilter(nums):
    special_numbers = 0

    for num in nums:
        # Convert to absolute value in case number is negative
        num_str = str(abs(num))
        
        # Check if number > 10 and first digit and last digit are odd
        if num > 10 and int(num_str[0]) % 2 != 0 and int(num_str[-1]) % 2 != 0:
            special_numbers += 1

    return special_numbers
