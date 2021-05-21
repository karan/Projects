#!/usr/local/bin/python3
'''
Kinda working PI calculator...
'''

import sys

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


def main():
        if len(sys.argv) < 2:
            print(f"[*] Usage {sys.argv[0]} <Tries> ")
            raise SystemExit
        try:
            PI(2,int(sys.argv[1]))
        except:
            print("[*] Invalid argument")
            raise SystemExit

if __name__ == "__main__": main()

# x = 2
#  x = 4
#  x = 6