
def sort_array(arr):
    arr.sort(key=lambda x: (bin(x).count('1'), x))
    return arr
