
def compare(game, guess):
    # Calculate the absolute difference between each pair of elements in the given lists
    return [abs(x - y) for x, y in zip(game, guess)]
