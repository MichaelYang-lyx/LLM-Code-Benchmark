
def fruit_distribution(s,n):
    words = s.split() #Splitting the string into a list of words
    apples = int(words[0]) #Number of apples 
    oranges = int(words[3]) #Number of oranges
    mangoes = n - apples - oranges #Calculating mangoes
    return mangoes #Returning number of mangoes
