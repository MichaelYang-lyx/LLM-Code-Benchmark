
def is_equal_to_sum_even(n):
    """Evaluate whether the given number n can be written as the sum of exactly 4 positive even numbers
    Example
    is_equal_to_sum_even(4) == False
    is_equal_to_sum_even(6) == False
    is_equal_to_sum_even(8) == True
    """
    # Since the smallest even positive number is 2, n must be at least 4*2=8 to be written as the sum of 4 even numbers.
    if n < 8:
        return False
    
    # If n is not a multiple of 2, it cannot be the sum of even numbers.
    if n % 2 != 0:
        return False
    
    # Since 4 positive even numbers is the condition, n must be, at minimum, a multiple of 4*2=8.
    return n % 8 == 0
