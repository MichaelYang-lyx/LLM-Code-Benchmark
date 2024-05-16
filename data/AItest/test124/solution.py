
def split_words(txt):
    '''
    Given a string of words, return a list of words split on whitespace, if no whitespaces exists in the text you
    should split on commas ',' if no commas exists you should return the number of lower-case letters with odd order in the
    alphabet, ord('a') = 1, ord('b') = 2, ... ord('z') = 26
    Examples
    split_words("Hello world!") --> ["Hello", "world!"]
    split_words("Hello,world!") --> ["Hello", "world!"]
    split_words("abcdef") == 3 
    '''
    if ' ' in txt:
        return txt.split(' ')
    elif ',' in txt:
        return txt.split(',')
    else:
        return len([c for c in txt if c.islower() and (ord(c) - ord('a')) % 2 == 0])
