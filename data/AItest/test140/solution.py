
import re

def file_name_check(file_name):
    splitted_file = file_name.split('.')
    valid_extensions = ['txt', 'exe', 'dll']
    
    if len(splitted_file) != 2 or not splitted_file[0] or not splitted_file[0][0].isalpha() or splitted_file[1] not in valid_extensions:
        return 'No'

    digit_count = len([char for char in file_name if char.isdigit()])
    if digit_count > 3:
        return 'No'
        
    return 'Yes'
    
print(file_name_check("example.txt"))  # => 'Yes'
print(file_name_check("1example.dll"))  # => 'No' (the name should start with a latin alphabet letter)
