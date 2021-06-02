#!/usr/local/bin/python3
#calculate Euler (e) number
#**Find e to the Nth Digit** - Just like the previous problem, but with e instead of PI.
# Enter a number and have the program generate e up to that many decimal places.
# Keep a limit to how far the program will go.


# e = (1 + 1/n)n

from sys import argv
import decimal

def calculate_e(x):
    for n in range(1,x):
        e = decimal.Decimal(pow((1+1/n),n))
        yield e
        
def calculate_decimals(x):
    no = float(x)
    return len(str(no).split(".")[1])

def main():
    assert len(argv) == 2
    try:
        for e in calculate_e(10000000000000):
            dec = calculate_decimals(e)
            if dec == int(argv[1]):
                print(e)
                break
        
    except AssertionError as err:
        print(f"[*] Usage: {argv[0]} <decimals>")
        print(err)

if __name__ == "__main__": main()