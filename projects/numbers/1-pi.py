# Import math Library
import math

def __getNthDecimalOfPiFromMathModule__(n: int) -> float:
    return math.pi
    # a = pow(10, n)
    # return math.trunc(math.pi * a) / a

def test(expectedFunction: callable, testFunction: callable, n: int)  :
    expected = format(expectedFunction(n), f".{n+1}g")
    result = format(testFunction(n), f".{n+1}g")

    print(f"n={n}\nexpected: {expected}\nresult: {result}\n")
    return expected == result


def getNthDecimalOfPi(n) :
    """
    Find PI to the Nth Digit using BPP formula
    https://fr.wikipedia.org/wiki/Formule_BBP#Et_pour_le_calcul_des_d%C3%A9cimales_?
    """

    result = 0
    for k in range(n) :
        result += 1 / (16**k) * (4/(8*k + 1) - 2/(8*k+4) -1/(8*k +5) - 1/(8*k+6))
    return float(result)


for a in range(1, 10) : 
    assert test(__getNthDecimalOfPiFromMathModule__, getNthDecimalOfPi, a)
    print(f"Test {a} passed")