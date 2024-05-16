
def any_int(x, y, z):
    if isinstance(x, int) and isinstance(y, int) and isinstance(z, int):
        if x == y + z or y == x + z or z == x + y:
            return True
        else:
            return False
    else:
        return False

# Test cases
print(any_int(5, 2, 7)) # True
print(any_int(3, 2, 2)) # False
print(any_int(3, -2, 1)) # True
print(any_int(3.6, -2.2, 2)) # False
