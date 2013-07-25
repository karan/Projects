"""
Factorial Finder - The Factorial of a positive integer, n,
is defined as the product of the sequence n, n-1, n-2, ...1
and the factorial of zero, 0, is defined as being 1. Solve
this using both loops and recursion.
"""

def fact_loop(n):
    """
    Returns the factorial of a given positive, non-zero integer
    using loops.
    """
    fact = 1
    while n > 0:
        fact *= n
        n -= 1
    return fact

def fact_recursion(n):
    """
    Returns the factorial of a given positive, non-zero integer
    using recursion.
    """
    return 1 if n == 0 else n * fact_recursion(n - 1) # if user as ternary operator

if __name__ == '__main__':
    n = input('Enter a positive number: ')

    if n >= 0:
        print 'Factorial of %d by loops is %d' % (n, fact_loop(n))
        print 'Factorial of %d by recursion is %d' % (n, fact_recursion(n))
    else:
        print 'Not a valid number'
