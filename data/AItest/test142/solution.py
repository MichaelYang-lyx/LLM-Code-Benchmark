
import math
def words_in_sentence(sentence):
    def is_prime(n):
        if n <= 1:
            return False
        elif n == 2:
            return True
        elif n % 2 == 0:
            return False
        sqrt_n = math.isqrt(n)
        for i in range(3, sqrt_n + 1, 2):
            if n % i == 0:
                return False
        return True
    
    words = sentence.split(" ")
    words = [word for word in words if is_prime(len(word))]
    return " ".join(words)
