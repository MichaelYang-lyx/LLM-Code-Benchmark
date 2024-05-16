
def encrypt(s):
    encrypted = ''
    for char in s:
        # Check if the character is a lower case letter
        if char.islower():
            # Calculate the ASCII value of the new character
            new_char = chr((ord(char) - 97 + 4) % 26 + 97)
            encrypted += new_char
    return encrypted
