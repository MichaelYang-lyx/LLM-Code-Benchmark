
def compare(game, guess):
    return [abs(game[i] - guess[i]) if game[i] != guess[i] else 0 for i in range(len(game))]

print(compare([1,2,3,4,5,1],[1,2,3,4,2,-2]))  # Output: [0, 0, 0, 0, 3, 3]
print(compare([0,5,0,0,0,4],[4,1,1,0,0,-2]))  # Output: [4, 4, 1, 0, 0, 6]
