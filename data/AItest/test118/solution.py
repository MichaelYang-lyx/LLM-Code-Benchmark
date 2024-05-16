
def match_parens(lst):
    open_count = 0
    for s in lst:
        for char in s:
            if char == '(':
                open_count += 1
            else:
                if open_count > 0:
                    open_count -= 1
                else:
                    return 'No'
    
    if open_count == 0:
        return 'Yes'
    else:
        return 'No'

# Test cases
print(match_parens(['()(', ')']))  # Output: Yes
print(match_parens([')', ')']))     # Output: No
