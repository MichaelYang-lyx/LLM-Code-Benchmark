
import math

def largest_prime_factor(n: int):
    """Return the largest prime factor of n. Assume n > 1 and is not a prime.
    """

    # Initialize the maximum prime factor
    max_prime = -1
    
    # Print the number of 2s that divide n
    while n % 2 == 0:
        max_prime = 2
        n /= 2  
         
    # n must be odd at this point, thus skip the even numbers and iterate only for odd
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            max_prime = i
            n = n / i
             
    # This condition is to handle the case when n is a prime number greater than 2
    if n > 2:
        max_prime = n
     
    return int(max_prime)
    
print(largest_prime_factor(13195)) # output: 29
print(largest_prime_factor(2048))  # output: 2
