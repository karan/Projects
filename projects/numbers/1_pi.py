"""
1_pi
"""
# Import math Library
import math

def __get_nth_decimal_of_pi_from_math_module__(decimal: int) -> float:
    return round(math.pi, decimal)

def test(expected_function: callable, test_function: callable, decimal: int)  :
    """ Test """
    expected = expected_function(decimal)
    result = test_function(decimal)

    print(f"n={decimal}\nexpected: {expected}\nresult: {result}\n")
    return expected == result

def get_nth_decimal_of_pi(decimal: int) :
    """
    Find PI to the Nth Digit using BPP formula
    https://fr.wikipedia.org/wiki/Formule_BBP#Et_pour_le_calcul_des_d%C3%A9cimales_?
    """

    result = 0
    for k in range(decimal+1) :
        result += 1 / (16**k) * (4/(8*k + 1) - 2/(8*k+4) -1/(8*k +5) - 1/(8*k+6))
    return round(result, decimal)

for a in range(100) :
    assert test(__get_nth_decimal_of_pi_from_math_module__, get_nth_decimal_of_pi, a)
    print(f"Test {a} passed")
