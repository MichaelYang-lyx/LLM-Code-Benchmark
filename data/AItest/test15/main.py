from solution import greatest_common_divisor as candidate 
def main():
    assert candidate(3, 7) == 1
    assert candidate(10, 15) == 5
    assert candidate(49, 14) == 7
    assert candidate(144, 60) == 12

    return 1.0