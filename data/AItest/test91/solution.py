
def any_int(x, y, z):
    # first check that all numbers are integers using isinstance
    if not all(isinstance(i, int) for i in [x, y, z]):
        return False
    # check if one of the numbers is equal to the sum of the other two
    if x == y + z or y == x + z or z == x + y:
        return True
    # if none of the above conditions are met
    return False

print(any_int(5, 2, 7))   # True
print(any_int(3, 2, 2))   # False
print(any_int(3, -2, 1))  # True
print(any_int(3.6, -2.2, 2))  # False
