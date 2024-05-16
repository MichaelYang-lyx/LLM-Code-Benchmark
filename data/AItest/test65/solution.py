
def digitSum(s):
    sum = 0
    for char in s:
        if char.isupper():
            sum += ord(char)
    return sum
