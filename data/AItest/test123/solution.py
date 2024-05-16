
def valid_date(date):
    import re
    pattern = r'^(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])-(\d{4})$'
    if re.match(pattern, date):
        month, day, year = map(int, date.split('-'))
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return day <= 31
        elif month in [4, 6, 9, 11]:
            return day <= 30
        elif month == 2:
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                return day <= 29
            else:
                return day <= 28
    return False
