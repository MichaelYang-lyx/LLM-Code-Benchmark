
def find_max(words):
    max_unique_word = ""
    max_unique_count = 0

    # Sorts words in reverse lexicographical order
    words.sort(reverse=True)

    for word in words:
        unique_chars = set(word)
    
        # If the current word has more unique characters or 
        # if it has the same amount but is earlier in lexicographical order
        if len(unique_chars) > max_unique_count or (len(unique_chars) == max_unique_count and word < max_unique_word):
            max_unique_word = word
            max_unique_count = len(unique_chars)

    return max_unique_word

print(find_max(["name", "of", "string"]))  # Outputs: 'string'
print(find_max(["name", "enam", "game"]))  # Outputs: 'enam'
print(find_max(["aaaaaaa", "bb" ,"cc"]))  # Outputs: 'aaaaaaa'
