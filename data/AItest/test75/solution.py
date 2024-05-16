
def is_simple_power(x, n):
    if x == 1:
        return True
    if n == 1:
        return False
    power = n
    while power < x:
        power *= n
    return power == x
