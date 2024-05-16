
from typing import List

def sort_numbers(numbers: str) -> str:
    num_dict = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
    reverse_dict = {v: k for k, v in num_dict.items()}
    
    split_numbers = numbers.split()
    numeric_numbers = [num_dict[num] for num in split_numbers]
    
    sorted_numbers = sorted(numeric_numbers)
    
    return " ".join([reverse_dict[num] for num in sorted_numbers])
