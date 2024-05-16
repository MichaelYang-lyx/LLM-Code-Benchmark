
def correct_bracketing(brackets: str) -> bool:
    stack = []
    for bracket in brackets:
        if bracket == '<':  
            stack.append(bracket)  
        else: # is '>'
            if len(stack) == 0:
                return False
            stack.pop()
    return len(stack) == 0

# Testing
print(correct_bracketing("<"))
print(correct_bracketing("<>"))
print(correct_bracketing("<<><>>"))
print(correct_bracketing("><<>"))
