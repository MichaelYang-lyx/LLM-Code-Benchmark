
def eat(number, need, remaining):
    total_eaten = number + need
    if total_eaten <= remaining:
        carrots_left = remaining - total_eaten
    else:
        carrots_left = 0
    return [total_eaten, carrots_left]

# Test cases
print(eat(5, 6, 10))  # Output: [11, 4]
print(eat(4, 8, 9))   # Output: [12, 1]
print(eat(1, 10, 10)) # Output: [11, 0]
print(eat(2, 11, 5))  # Output: [7, 0]
