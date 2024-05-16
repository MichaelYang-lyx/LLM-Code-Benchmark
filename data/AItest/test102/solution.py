
def rounded_avg(n, m):
    if n > m:
        return -1
    s = sum(range(n, m+1))
    avg = round(s / (m-n+1))
    return bin(avg)
