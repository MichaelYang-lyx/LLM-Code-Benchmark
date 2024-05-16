
def histogram(test):
    """Given a string representing a space separated lowercase letters, return a dictionary
    of the letter with the most repetition and containing the corresponding count.
    If several letters have the same occurrence, return all of them.
    
    Example:
    histogram('a b c') == {'a': 1, 'b': 1, 'c': 1}
    histogram('a b b a') == {'a': 2, 'b': 2}
    histogram('a b c a b') == {'a': 2, 'b': 2}
    histogram('b b b b a') == {'b': 4}
    histogram('') == {}

    """
    
    letters = test.split()
    letter_count = {}
    
    for letter in letters:
        if letter in letter_count:
            letter_count[letter] += 1
        else:
            letter_count[letter] = 1
    
    max_count = max(letter_count.values())
    most_repeated = {key: value for key, value in letter_count.items() if value == max_count}
    
    return most_repeated
