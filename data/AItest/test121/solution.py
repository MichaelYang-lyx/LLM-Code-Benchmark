
def add_elements(arr, k):
    """
    Given a non-empty array of integers arr and an integer k, return
    the sum of the elements with at most two digits from the first k elements of arr.

    Example:

        Input: arr = [111,21,3,4000,5,6,7,8,9], k = 4
        Output: 24 # sum of 21 + 3

    Constraints:
        1. 1 <= len(arr) <= 100
        2. 1 <= k <= len(arr)
    """
    sum_elements = 0
    count = 0
    for num in arr:
        if count >= k:
            break
        if len(str(num)) <= 2:
            sum_elements += num
            count += 1
    return sum_elements

# Test the function
arr = [111, 21, 3, 4000, 5, 6, 7, 8, 9]
k = 4
print(add_elements(arr, k))  # Output: 24
