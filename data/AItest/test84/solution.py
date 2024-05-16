
def add(lst):
    sum_of_evens = 0
    for i in range(len(lst)):
        if i % 2 != 0 and lst[i] % 2 == 0:
            sum_of_evens += lst[i]
    return sum_of_evens

print(add([4, 2, 6, 7]))  # Extension of your example
