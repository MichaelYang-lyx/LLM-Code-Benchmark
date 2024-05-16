
from typing import List, Tuple

def rolling_max(numbers: List[int]) -> List[int]:
    if not numbers: return []
    max_number = numbers[0]
    result = []
    for num in numbers:
        if num > max_number:
            max_number = num
        result.append(max_number)
    return result
