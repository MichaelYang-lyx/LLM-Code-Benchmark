
def count_up_to(n):
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    return [x for x in range(2, n) if is_prime(x)]
