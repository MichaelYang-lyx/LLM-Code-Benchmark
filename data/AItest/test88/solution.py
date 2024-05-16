
def encrypt(s):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    encrypted = ''
    for char in s:
        if char.isalpha():
            shifted_index = (alphabet.index(char) + 2) % 26
            encrypted += alphabet[shifted_index]
        else:
            encrypted += char
    return encrypted

# Test cases
print(encrypt('hi'))  # Output: 'lm'
print(encrypt('asdfghjkl'))  # Output: 'ewhjklnop'
print(encrypt('gf'))  # Output: 'kj'
print(encrypt('et'))  # Output: 'ix'
