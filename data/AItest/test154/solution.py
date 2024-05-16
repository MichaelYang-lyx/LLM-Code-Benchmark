
def even_odd_count(num):
    """Given an integer. return a tuple that has the number of even and odd digits respectively.

     Example:
        even_odd_count(-12) ==> (1, 1)
        even_odd_count(123) ==> (1, 2)
    """
    
    num = abs(num)  # convert to positive if number is negative
    nums = [int(i) for i in str(num)]  # create a list of digits
    
    even_count = sum(i % 2 == 0 for i in nums)
    odd_count = sum(i % 2 != 0 for i in nums)
    
    return even_count, odd_count
