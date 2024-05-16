
def is_simple_power(x, n):
    if x == 1:
        return True
    else:
        return x == n**int(x**(1/n))

print(is_simple_power(1, 4))  # Expected Output: True
print(is_simple_power(2, 2))  # Expected Output: True
print(is_simple_power(8, 2))  # Expected Output: True
print(is_simple_power(3, 2))  # Expected Output: False
print(is_simple_power(3, 1))  # Expected Output: False
print(is_simple_power(5, 3))  # Expected Output: False
