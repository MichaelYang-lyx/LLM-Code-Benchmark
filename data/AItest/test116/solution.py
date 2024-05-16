
def select_words(s, n):
    def count_consonants(word):
        vowels = 'aeiouAEIOU'
        return sum(1 for letter in word if letter.isalpha() and letter not in vowels)
    
    words = s.split()
    result = [word for word in words if count_consonants(word) == n]
    return result
