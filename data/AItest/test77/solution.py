
def hex_key(num):
    """ Function to count prime hexadecimal digits """
    # Define prime hexadecimal digits
    prime_hex_digits = '2357BD'
    
    # Convert input string to upper case (to ensure that 'b' and 'd' are also accounted for)
    num = num.upper()
    
    # Count prime hexadecimal digits
    cnt = sum( [1 for char in num if char in prime_hex_digits] )
    return cnt

# Test cases from the prompt
print(hex_key("AB"))  # should return 1
print(hex_key("1077E"))  # should return 2
print(hex_key("ABED1A33"))  # should return 4
print(hex_key("123456789ABCDEF0"))  # should return 6
print(hex_key("2020"))  # should return 2
