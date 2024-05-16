
def cycpattern_check(a , b):
    len_b = len(b)
    b_rotated = b

    for i in range(len_b):
        if b_rotated in a:
            return True
        else:
            b_rotated = b_rotated[1:] + b_rotated[0] #rotate string

    return False
