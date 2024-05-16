
def smallest_change(arr):
    start = 0
    end = len(arr) - 1
    changes = 0

    while start < end:
        if arr[start] != arr[end]:
            changes += 1
        start += 1
        end -= 1

    return changes
