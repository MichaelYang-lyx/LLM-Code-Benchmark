
def right_angle_triangle(a, b, c):
    '''
    Given the lengths of the three sides of a triangle. Return True if the three
    sides form a right-angled triangle, False otherwise.
    A right-angled triangle is a triangle in which one angle is a right angle or 
    90 degrees.
    Example:
    right_angle_triangle(3, 4, 5) == True
    right_angle_triangle(1, 2, 3) == False
    '''
    sides = [a, b, c]
    sides.sort()
    if sides[0]**2 + sides[1]**2 == sides[2]**2:
        return True
    else:
        return False
