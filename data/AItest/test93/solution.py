
def is_prime(n):
    if n == 0 or n == 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def skjkasdkd(lst):
    # Return 0 immediately if the list is empty
    if not lst:
        return 0

    # Find the largest prime number
    max_prime = max((num for num in lst if is_prime(num)), default=0)

    # Return the sum of its digits
    return sum(int(digit) for digit in str(max_prime))
