
def reverse_delete(s,c):
    result = ''.join([i for i in s if i not in c])
    return result, result == result[::-1]
