
import re

def get_closest_vowel(word):
    vowels = "aeiouAEIOU"
    for i in range(len(word) - 1, 0, -1):
        if word[i] in vowels and re.match(r"[^aeiouAEIOU]{2}", word[i-1:i+1]):
            return word[i]
    return ""
