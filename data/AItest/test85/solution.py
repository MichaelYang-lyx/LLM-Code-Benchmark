
def anti_shuffle(s):
    words = s.split()
    ordered_words = []
    for word in words:
        sorted_word = ''.join(sorted(word))
        ordered_words.append(sorted_word)
    return ' '.join(ordered_words)

# Test cases
print(anti_shuffle('Hi')) # 'Hi'
print(anti_shuffle('hello')) # 'ehllo'
print(anti_shuffle('Hello World!!!')) # 'Hello !!!Wdlor'
