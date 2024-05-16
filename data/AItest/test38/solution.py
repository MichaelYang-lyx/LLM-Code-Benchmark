
def sort_even(l: list):
    """This function takes a list l and returns a list l' such that
    l' is identical to l in the odd indicies, while its values at the even indicies are equal
    to the values of the even indicies of l, but sorted.
    """
    evens = sorted(l[i] for i in range(0, len(l), 2))
    result = l.copy()
    for i in range(0, len(l), 2):
        result[i] = evens.pop(0)
    return result

print(sort_even([1, 2, 3]))
print(sort_even([5, 6, 3, 4]))
