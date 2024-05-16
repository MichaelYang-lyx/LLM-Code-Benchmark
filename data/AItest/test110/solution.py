
def histogram(test):
    """Given a string representing a space separated lowercase letters, return a dictionary
    of the letter with the most repetition and containing the corresponding count.
    If several letters have the same occurrence, return all of them.
    """
    # Create a dictionary to hold letter occurrences.
    letter_counts = {}
    for letter in test.split():
        # Check if letter is in dictionary, if not add it with count 1, otherwise increment the count.
        if letter not in letter_counts:
            letter_counts[letter] = 1
        else:
            letter_counts[letter] += 1

    # Find the maximum count of any letter.
    max_count = max(letter_counts.values(), default=0)

    # Return a dictionary with only the letters with the maximum count.
    return {key: value for key, value in letter_counts.items() if value == max_count}
