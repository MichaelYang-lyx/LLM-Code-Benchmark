
def can_arrange(arr):
    greatest_idx = -1
    for i in range(1, len(arr)):
        if arr[i-1] > arr[i]:
            greatest_idx = i
    return greatest_idx
