#!/usr/local/bin/python3
'''
Kinda working PI calculator...
'''

import sys
from math import atan
import os

pi = 3
sys.setrecursionlimit(100000)

c = 0

def PI(x,counter):
        global pi, c
        try:
                if c < counter:
                        pi += 4/(x * (x+1) * (x+2))
                        x +=  2
                        pi -= 4/(x * (x+1) * (x+2))
                        print(pi)
                        c += 1
                        PI(x+2, counter)
        except Exception as e:
                print(e)


def PI_gregory_leibniz_series():
    # pi / 4 = 4 * arctan(1/5) - arctan(1/239)
    pi = 4 * atan(1/5) - atan(1/239)
    return pi * 4


def main():
        if len(sys.argv) < 2:
            print(f"[*] Usage {sys.argv[0]} <Tries> ")
            raise SystemExit
        try:
            if sys.argv[1] == "fast":
                pi = PI_gregory_leibniz_series()
                print(pi)
                os._exit(0)
            PI(2,int(sys.argv[1]))
        except:
            print("[*] Invalid argument")
            raise SystemExit

if __name__ == "__main__": main()

# x = 2
#  x = 4
#  x = 6