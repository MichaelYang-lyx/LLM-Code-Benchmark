
def largest_smallest_integers(lst):
    negative_integers = [i for i in lst if i < 0]
    positive_integers = [i for i in lst if i > 0]

    a = max(negative_integers) if negative_integers else None
    b = min(positive_integers) if positive_integers else None

    return (a, b)
