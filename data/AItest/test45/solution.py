
def triangle_area(a, h):
    """Given length of a side and high return area for a triangle."""
    if a <= 0 or h <= 0:
        return "Invalid side or height. Both must be greater than zero."
    else:
        area = 0.5 * a * h
        return area

#Test the function
print(triangle_area(5, 3))
