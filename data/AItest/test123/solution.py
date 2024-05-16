
def valid_date(date):
    if date == "":
        return False

    try:
        month, day, year = map(int, date.split('-'))

        if month < 1 or month > 12:
            return False

        if month in [4, 6, 9, 11]:
            if day < 1 or day > 30:
                return False
        elif month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                if day < 1 or day > 29:
                    return False
            else:
                if day < 1 or day > 28:
                    return False
        else:
            if day < 1 or day > 31:
                return False
                
        return True
                
    except ValueError:
        return False
