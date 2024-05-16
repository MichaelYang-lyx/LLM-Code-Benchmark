
def check_dict_case(dict):
    """
    Given a dictionary, return True if all keys are strings in lower 
    case or all keys are strings in upper case, else return False.
    The function should return False is the given dictionary is empty.
    The function should also return False if there are non-string keys.
    """
    if not dict:
        return False

    keys = list(dict.keys())
    
    # Check if there are non-string keys
    for key in keys:
        if not isinstance(key, str):
            return False

    # Check if all keys are in lower case or in upper case
    lower_case = all(key.islower() for key in keys)
    upper_case = all(key.isupper() for key in keys)

    return lower_case or upper_case
