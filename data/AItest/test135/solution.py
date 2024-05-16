
def largest_smallest_integers(lst):
    neg_ints = [i for i in lst if i < 0]
    pos_ints = [i for i in lst if i > 0]
    
    if not neg_ints:
        max_neg = None
    else:
        max_neg = max(neg_ints)
        
    if not pos_ints:
        min_pos = None
    else:
        min_pos = min(pos_ints)
        
    return (max_neg, min_pos)

# Test cases
print(largest_smallest_integers([2, 4, 1, 3, 5, 7]))  # Output: (None, 1)
print(largest_smallest_integers([]))  # Output: (None, None)
print(largest_smallest_integers([0]))  # Output: (None, None)
