
def median(l: list):
    n = len(l)
    if n == 0:
        raise ValueError("The list is empty")
    sorted_l = sorted(l)
    mid = n // 2
    if n % 2 == 1:
        # if odd, return the middle value
        return sorted_l[mid]
    else:
        # if even, return the average of the two middle values
        return (sorted_l[mid - 1] + sorted_l[mid]) / 2
