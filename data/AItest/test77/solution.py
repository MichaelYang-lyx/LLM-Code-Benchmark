
def hex_key(num):
    primes = {'2': True, '3': True, '5': True, '7': True, 'B': True, 'D': True}
    count = 0
    for char in num:
        if char in primes:
            count += 1
    return count
