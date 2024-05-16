
def check_dict_case(dict):
    if len(dict) == 0:
        return False
    lower_case = all(key.islower() for key in dict.keys())
    upper_case = all(key.isupper() for key in dict.keys())
    return lower_case or upper_case
