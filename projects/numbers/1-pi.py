# Import math Library
import math
import decimal

def __getNthDecimalOfPiFromMathModule__(n: int) -> float:
    a = pow(10, n)
    return math.trunc(math.pi * a) / a

def test(f: callable, n: int)  :
    return __getNthDecimalOfPiFromMathModule__(n) == f(n)


def getNthDecimalOfPi(n) :
    """
    Find PI to the Nth Digit using BPP formula
    https://fr.wikipedia.org/wiki/Formule_BBP#Et_pour_le_calcul_des_d%C3%A9cimales_?
    """
    result = 0
    for k in range(n) :
        result += 1 / (16**k) * (4/(8*k + 1) - 2/(8*k+4) -1/(8*k +5) - 1/(8*k+6))
    return result


for a in range(1000) : 
    assert test(getNthDecimalOfPi, 1) != True
    print(f"Test {a} passed")