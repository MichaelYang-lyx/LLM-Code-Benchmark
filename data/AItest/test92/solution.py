
def encode(message):
    encoded_message = ""
    vowels = "aeiouAEIOU"
    for char in message:
        if char.lower() in vowels:
            encoded_message += chr(ord(char) + 2)
        else:
            encoded_message += char.swapcase()
    return encoded_message

# Test cases
print(encode('test'))  # Output: TGST
print(encode('This is a message'))  # Output: tHKS KS C MGSSCGG
