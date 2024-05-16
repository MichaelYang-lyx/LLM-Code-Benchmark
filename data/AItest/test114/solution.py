
def max_fill(grid, capacity):
    import math
    # Count total amount of water
    total_water = sum(sum(row) for row in grid)
    
    # Calculate total number of full-capacity buckets needed
    total_buckets = math.ceil(total_water / capacity)
    
    return total_buckets
