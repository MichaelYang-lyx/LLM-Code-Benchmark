
def cycpattern_check(a, b):
    if len(a) != len(b):
        return False
    double_a = a + a
    return b in double_a
