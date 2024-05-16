
def solve(s):
    if any(char.isalpha() for char in s):
        return "".join(char.swapcase() if char.isalpha() else char for char in s)
    else:
        return s[::-1]

print(solve("1234"))  # Output: "4321"
print(solve("ab"))  # Output: "AB"
print(solve("#a@C"))  # Output: "#A@c"
