
def choose_num(x, y):
    max_num = -1
    for num in range(x, y+1):
        if num % 2 == 0 and num > max_num:
            max_num = num
    return max_num
