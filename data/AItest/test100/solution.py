
def words_string(s):
    words = s.replace(',', ' ').split()
    return words

print(words_string("Hi, my name is John"))  # Output: ["Hi", "my", "name", "is", "John"]
print(words_string("One, two, three, four, five, six"))  # Output: ["One", "two", "three", "four", "five", "six"]
