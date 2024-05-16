
def triples_sum_to_zero(l: list):

    l.sort()
    n = len(l)
    for i in range(n-2):
        if i > 0 and l[i] == l[i-1]:
            continue
            
        left = i + 1
        right = n - 1
        
        while left < right:
            total = l[i] + l[left] + l[right]
            
            if total > 0:
                right -= 1
            elif total < 0:
                left += 1
            else:
                return True
            
    return False
