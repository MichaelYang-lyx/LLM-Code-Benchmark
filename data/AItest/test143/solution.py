
from fractions import Fraction

def simplify(x, n):
    multiplied_fraction = Fraction(x) * Fraction(n)
    return multiplied_fraction.denominator == 1

print(simplify("1/5", "5/1"))   # True
print(simplify("1/6", "2/1"))   # False
print(simplify("7/10", "10/2")) # False
