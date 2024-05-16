
import re

def check_if_last_char_is_a_letter(txt):
    if txt == "":
        return False
    else:
        last_char = txt[-1]
        if last_char.isalpha() and re.match(r'\b\w+\b', txt) is None:
            return True
        else:
            return False
