
def is_bored(S):
    """
    You'll be given a string of words, and your task is to count the number
    of boredoms. A boredom is a sentence that starts with the word "I".
    Sentences are delimited by '.', '?' or '!'.

    For example:
    >>> is_bored("Hello world")
    0
    >>> is_bored("The sky is blue. The sun is shining. I love this weather")
    1
    """
    # Splitting the text into sentences
    sentences = [s.strip() for s in re.split('[.!?]', S)]
    
    # Initializing the count of boredoms
    boredoms = 0

    # For each sentence
    for sentence in sentences:
        # If the sentence begins with "I", increase the boredom count
        if sentence.startswith("I"):
            boredoms += 1
    
    # Return the count of boredoms
    return boredoms
