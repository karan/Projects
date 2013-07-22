# Prime Factorization - Have the user enter a number
# and find all Prime Factors (if there are any) and
# display them.

import math

def is_a_prime(x):
    w = math.sqrt(x)
    if x%2 == 0:
        return False
    else:
        for i in range(3, w, 2):
            if x % i == 0:
                return False
        return True

# standard boilerplate
if __name__ == '__main__':
    n = int(raw_input('Enter the number to find prime factors of: '))

    factors = []

    for i in range(2, n + 1):
        if n % i == 0:
            if is_a_prime(i):
                factors.append(i)
                n /= i
    print factors
