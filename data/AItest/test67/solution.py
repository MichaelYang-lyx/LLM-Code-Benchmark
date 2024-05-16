
def pluck(arr):
    even_nodes = [(value, index) for index, value in enumerate(arr) if value % 2 == 0]
    
    if not even_nodes:
        return []
    
    min_even = min(even_nodes, key=lambda x: (x[0], x[1]))
    return [min_even[0], min_even[1]]

# Test the function
print(pluck([4,2,3]))  # Output: [2, 1]
print(pluck([1,2,3]))  # Output: [2, 1]
print(pluck([]))  # Output: []
print(pluck([5, 0, 3, 0, 4, 2]))  # Output: [0, 1]
