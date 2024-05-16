
def file_name_check(file_name):
    import re
    pattern = "^[a-zA-Z][a-zA-Z0-9]*\.[txt|exe|dll]{3}$"
    if re.match(pattern, file_name) and file_name.count('.') == 1 and file_name.count('0') + file_name.count('1') + file_name.count('2') + file_name.count('3') + file_name.count('4') + file_name.count('5') + file_name.count('6') + file_name.count('7') + file_name.count('8') + file_name.count('9') <= 3:
        return 'Yes'
    else:
        return 'No'
