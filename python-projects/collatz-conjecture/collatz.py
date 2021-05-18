#!/usr/local/bin/python3
'''
Collatz Conjecture - Start with a number n > 1. Find the number of steps it takes to reach one using the following process: If n is even, divide it by 2. If n is odd, multiply it by 3 and add 1.
'''
import sys
from datetime import datetime

def collatz(n):
    steps = 0
    assert n > 1
    t = datetime.now()
    try:
        while n != 1:
            if n % 2 == 0:
                n = n / 2
                steps += 1
                print(n)
            elif n % 2 != 0:
                n = n * 3 + 1
                steps += 1
                print(n)
        t_final = datetime.now() - t
        return (steps,t_final)
    except AssertionError as e:
        print(e)

def main():
    if len(sys.argv) < 2:
        print("[*] Usage", sys.argv[0],"<N>")
        sys.exit(-1)
    n = float(sys.argv[1])
    steps, t = collatz(n)
    print("[*] There were required" ,steps, "steps")
    print("[*] Time passed", t)
    
if __name__ == "__main__": main()
        