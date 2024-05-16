
def count_upper(s):
    count = 0
    vowels = ['A', 'E', 'I', 'O', 'U']
    for i in range(0, len(s), 2):
        if s[i] in vowels:
            count += 1
    return count

# Test cases
print(count_upper('aBCdEf'))  # Output: 1
print(count_upper('abcdefg'))  # Output: 0
print(count_upper('dBBE'))     # Output: 0
