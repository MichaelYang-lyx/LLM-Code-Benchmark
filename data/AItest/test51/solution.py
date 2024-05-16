
def below_threshold(l: list, t: int) -> bool:
    """Return True if all numbers in the list l are below threshold t."""

    return all(elem < t for elem in l)

# Testing the function
print(below_threshold([1, 2, 4, 10], 100)) # Expected: True
print(below_threshold([1, 20, 4, 10], 5))  # Expected: False
