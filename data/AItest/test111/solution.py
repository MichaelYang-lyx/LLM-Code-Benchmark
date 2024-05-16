
def reverse_delete(s, c):
    res = ''.join([i for i in s if i not in c]) # Removing characters in s that are in c
    return (res, res == res[::-1]) #Returning the result string and checking if it is a palindrome

print(reverse_delete("abcde", "ae")) 
print(reverse_delete("abcdef", "b"))
print(reverse_delete("abcdedcba", "ab"))
