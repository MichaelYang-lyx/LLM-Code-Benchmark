
def prod_signs(arr):
    if not arr:
        return None

    sign_product = 1
    magnitude_sum = 0

    for num in arr:
        if num < 0:
            sign_product *= -1
            magnitude_sum += abs(num) # update magnitude sum
        elif num > 0:
            magnitude_sum += num # update magnitude sum
        else:
            sign_product = 0  # product will be zero if we have 0 in array
            break  # no need to iterate more as we got 0 in array

    return sign_product * magnitude_sum
