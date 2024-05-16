
import hashlib

def string_to_md5(text):
    if text:
        return hashlib.md5(text.encode()).hexdigest()
    else:
        return None

# Test
print(string_to_md5('Hello world'))  # Output: 3e25960a79dbc69b674cd4ec67a72c62
