
def by_length(arr):
    numbers = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}
    arr = [x for x in arr if 1 <= x <= 9]
    arr.sort()
    arr.reverse()
    result = [numbers[x] for x in arr]
    return result
