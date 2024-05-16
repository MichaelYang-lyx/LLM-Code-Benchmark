
def exchange(lst1, lst2):
    if sum(x % 2 for x in lst1) > sum(x % 2 for x in lst2):
        return "NO"
    return "YES"
