
def even_odd_palindrome(n):
    if not(1 <= n <= 10**3):
        return "Input should be in the range from 1 to 10^3"
    
    even = 0
    odd = 0
    for i in range(1, n+1):
        if str(i) == str(i)[::-1]:
            if i % 2 == 0 :
                even += 1
            else:
                odd += 1
    return even, odd
