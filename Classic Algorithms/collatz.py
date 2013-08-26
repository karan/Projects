"""
Collatz Conjecture - Start with a number n > 1.
Find the number of steps it takes to reach one using
the following process: If n is even, divide it by 2.
If n is odd, multiply it by 3 and add 1.
"""

def main():
    try:
        n = int(raw_input('Enter a number: '))
    except ValueError:
        print 'Enter only an integer value, n > 1.'

    steps = 0

    print '\n%d' % n,
    
    while n > 1:
        if n % 2 == 0:
            n /= 2
        else:
            n = (n * 3) + 1
        steps += 1
        print ' -> %d' % n,
        
    print '\n\n%d steps take to reach ONE.' % steps

if __name__ == '__main__':
    main()
