
import math

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def words_in_sentence(sentence):
    words = sentence.split()
    prime_words = [word for word in words if is_prime(len(word))]
    return ' '.join(prime_words)

# Example 1
sentence1 = "This is a test"
print(words_in_sentence(sentence1))  # Output: "is"

# Example 2
sentence2 = "lets go for swimming"
print(words_in_sentence(sentence2))  # Output: "go for"
