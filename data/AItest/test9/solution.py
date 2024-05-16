
from typing import List

def parse_nested_parens(paren_string: str) -> List[int]:
    result = []
    for group in paren_string.split():
        level = 0
        max_level = 0
        for char in group:
            if char == '(':
                level += 1
            else:
                if level > max_level:
                    max_level = level
                level -= 1
        result.append(max_level)
    return result
