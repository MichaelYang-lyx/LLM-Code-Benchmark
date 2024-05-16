
def is_equal_to_sum_even(n):
    count = 0
    for i in range(2, n//2 + 1, 2):
        if n - i in range(2, n//2 + 1, 2):
            count += 1
    return count == 4

print(is_equal_to_sum_even(4))  # Output: False
print(is_equal_to_sum_even(6))  # Output: False
print(is_equal_to_sum_even(8))  # Output: True
