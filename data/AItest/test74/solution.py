
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def is_multiply_prime(a):
    prime_count = 0
    for i in range(2, a):
        if is_prime(i) and a % i == 0:
            prime_count += 1
    return prime_count == 3

# Test the function
print(is_multiply_prime(30))  # Output: True
