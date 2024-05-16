
from typing import List, Tuple

def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
    
    sorted_numbers = sorted(numbers)
    min_pairs = (sorted_numbers[0], sorted_numbers[1])
    min_diff = sorted_numbers[1] - sorted_numbers[0]

    for i in range(len(sorted_numbers) - 1):
        if sorted_numbers[i+1] - sorted_numbers[i] < min_diff:
            min_diff = sorted_numbers[i+1] - sorted_numbers[i]
            min_pairs = (sorted_numbers[i], sorted_numbers[i+1])

    return min_pairs
