#!/usr/local/bin/python3
#calculate Euler (e) number
#**Find e to the Nth Digit** - Just like the previous problem, but with e instead of PI.
# Enter a number and have the program generate e up to that many decimal places.
# Keep a limit to how far the program will go.


# e = (1 + 1/n)n

from sys import argv
import decimal
from datetime import datetime

def calculate_e(x):
    decimal.getcontext().prec = int(argv[1]) + 1
    for n in range(1,x):
        e = decimal.Decimal(pow((decimal.Decimal(1)+decimal.Decimal(1)/decimal.Decimal(n)),n))
        yield e

def main():
    assert len(argv) == 2
    PREC_NO = 500
    try:
        t = datetime.now()
        for e in calculate_e(PREC_NO):
            euler_no = e
        print(euler_no)
        t_final = datetime.now() - t
        print("[*] Time passed: ", t_final)
        
    except AssertionError as err:
        print(f"[*] Usage: {argv[0]} <decimals>")
        print(err)

if __name__ == "__main__": main()