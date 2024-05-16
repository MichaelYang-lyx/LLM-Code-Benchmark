
def encode(message):
    encoded_message = ""

    #defining vowels
    vowels = "aeiouAEIOU"
    mapping = {v: chr(ord(v) + 2) for v in vowels}
    
    #iterating the case of each character
    for char in message:
        if char.isalpha():
            if char in vowels:
                # replace vowels with the letter that appears 2 places ahead
                encoded_message += mapping[char]
            else:
                # swap case of all other letters
                encoded_message += char.swapcase()
        else:
            encoded_message += char

    return encoded_message
