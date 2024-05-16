
def right_angle_triangle(a, b, c):
    sides = sorted([a, b, c])
    return sides[2]**2 == sides[0]**2 + sides[1]**2
    
print(right_angle_triangle(3, 4, 5))  # True
print(right_angle_triangle(1, 2, 3))  # False
