
from fractions import Fraction

def simplify(x, n):
    x_frac = Fraction(x)
    n_frac = Fraction(n)
    result = x_frac * n_frac
    return result == int(result)
