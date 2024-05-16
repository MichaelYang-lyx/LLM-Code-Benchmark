
def match_parens(lst):
    def is_good(s):
        # a simple stack-based algorithm to check for balanced parentheses
        stack = []
        for c in s:
            if c == '(':
                stack.append(c)
            elif stack and stack[-1] == '(':
                stack.pop()
            else:
                return False
        return len(stack) == 0

    return 'Yes' if is_good(lst[0] + lst[1]) or is_good(lst[1] + lst[0]) else 'No'
