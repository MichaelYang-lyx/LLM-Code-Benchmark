
from typing import List


def intersperse(numbers: List[int], delimeter: int) -> List[int]:
    result = []
    for num in numbers:
        result.append(num)
        result.append(delimeter)
    result.pop()  # remove the extra delimiter at the end
    return result

# Test cases
print(intersperse([], 4))  # Output: []
print(intersperse([1, 2, 3], 4))  # Output: [1, 4, 2, 4, 3]
