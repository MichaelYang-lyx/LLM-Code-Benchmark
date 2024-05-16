
def make_a_pile(n):
    # initial list of stones
    stones = [n]
    # iterate over other levels
    for i in range(2, n + 1):
        # if the current number of stones is even
        if stones[-1] % 2 == 0:
            # append next even number
            stones.append(stones[-1] + 2)
        else:
            # append next odd number
            stones.append(stones[-1] + 2)
    return stones

# test the function
print(make_a_pile(3))  # should print: [3, 5, 7]
