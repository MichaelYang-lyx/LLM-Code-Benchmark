
def is_nested(string):
    # we'll store pairs of brackets in a stack, as we process the string
    stack = []
    for ch in string:
        # if this bracket opens a new pair, we add it to the stack
        if ch == '[':
            stack.append(ch)
        elif ch == ']':
            # if the stack is empty, the closing bracket does not match any opening bracket
            # so the string is not properly nested
            if not stack:
                return False
            # remove the last element from the stack (which has to be '[')
            last_bracket = stack.pop()
    # a string is properly nested if and only if the stack is empty at the end
    if len(stack) != 0:
        return False
    # check for nested brackets, which means there must be at least two sequential pairs of brackets
    if '[]' in string:
        return True
    return False
