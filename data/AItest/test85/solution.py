
def anti_shuffle(s):
    words = s.split(' ')
    sorted_words = [''.join(sorted(word)) for word in words]
    return ' '.join(sorted_words)
