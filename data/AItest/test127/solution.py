
from functools import reduce

def prod_signs(arr):
    if not arr:
        return None
    
    product = reduce(lambda x, y: x * y, arr)
    sum_magnitudes = sum(abs(num) for num in arr)
    
    return product * sum_magnitudes
