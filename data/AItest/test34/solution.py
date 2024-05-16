
def sort_third(l: list):
    sorted_indices = [i for i in range(len(l)) if i % 3 == 0]
    sorted_values = [l[i] for i in sorted_indices]
    sorted_values.sort()
    
    result = l.copy()
    for i in sorted_indices:
        result[i] = sorted_values.pop(0)
    
    return result
