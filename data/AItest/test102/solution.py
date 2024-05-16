
def rounded_avg(n, m):
    if n > m:
        return -1
    else:
        average = round((n + m) / 2)
        return bin(average)
