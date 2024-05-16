
def will_it_fly(q, w):
    if q == q[::-1] and sum(q) <= w:
        return True
    else:
        return False

# Test the function with the provided examples
print(will_it_fly([1, 2], 5))  # Should print: False 
print(will_it_fly([3, 2, 3], 1))  # Should print: False
print(will_it_fly([3, 2, 3], 9))  # Should print: True
print(will_it_fly([3], 5))   # Should print: True
