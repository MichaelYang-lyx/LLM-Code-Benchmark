
import math

def sum_squares(lst):
    total = 0
    for num in lst:
        total += math.ceil(num)**2
    return total
