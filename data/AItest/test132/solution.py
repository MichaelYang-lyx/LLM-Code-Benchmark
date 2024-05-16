
import math

def sum_squares(lst):
    result = 0
    for number in lst:
        result += math.pow(math.ceil(number), 2)
    return int(result)
