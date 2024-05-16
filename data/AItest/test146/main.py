from solution import get_max_triples as candidate 
def main():

    assert candidate(5) == 1
    assert candidate(6) == 4
    assert candidate(10) == 36
    assert candidate(100) == 53361

    return 1.0