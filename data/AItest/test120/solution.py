
def solution(lst):
    return sum(num for num in lst[1::2] if num % 2 != 0)
