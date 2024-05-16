
def count_nums(arr):
    def get_signed_digits(num):
        if num < 0:
            num = -num
            signed_digits = [-int(d) for d in str(num) if d.isdigit()]
            signed_digits[0] = -signed_digits[0]
        else:
            signed_digits = [int(d) for d in str(num) if d.isdigit()]
        return signed_digits

    def sum_digits(num):
        return sum(get_signed_digits(num))

    count = 0
    for num in arr:
        if sum_digits(num) > 0:
            count += 1

    return count

# Testing the function with the given test cases
print(count_nums([])) # Output: 0
print(count_nums([-1, 11, -11])) # Output: 1
print(count_nums([1, 1, 2])) # Output: 3
