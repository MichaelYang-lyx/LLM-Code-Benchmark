
def sort_even(l: list):
    even_indices = [l[i] for i in range(len(l)) if i % 2 == 0]
    sorted_even_indices = sorted(even_indices)
    result = [sorted_even_indices[i//2] if i % 2 == 0 else l[i] for i in range(len(l))]
    return result
