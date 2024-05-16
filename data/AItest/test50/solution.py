
def remove_vowels(text):
    vowels = 'aeiouAEIOU'
    return ''.join([i for i in text if not i in vowels])
