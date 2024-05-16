
def prime_length(string):
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, num):
            if num % i == 0:
                return False
        
        return True

    return is_prime(len(string))

print(prime_length('Hello')) # True
print(prime_length('abcdcba')) # True
print(prime_length('kittens')) # True
print(prime_length('orange')) # False
