"""
Happy Numbers - A happy number is defined by the
following process. Starting with any positive integer,
replace the number by the sum of the squares of its
digits, and repeat the process until the number equals
1 (where it will stay), or it loops endlessly in a
cycle which does not include 1. Those numbers for which
this process ends in 1 are happy numbers, while those
that do not end in 1 are unhappy numbers. Take an input
number from user, and find first 8 happy numbers from
that input.
"""

NUMBERS_REQUIRED = 8 # number of happy numbers required

def is_happy_number(num):
    seen = []
    while True:
        sum_digits = sum(int(digit) ** 2 for digit in str(num))
        if sum_digits == 1:
            return True
        elif sum_digits in seen:
            return False
        else:
            num = sum_digits
            seen.append(num)

if __name__ == '__main__':

    happies = [] # list of happy numbers found

    num = input('Start at: ')

    while len(happies) != NUMBERS_REQUIRED:
        if is_happy_number(num):
            happies.append(num)
        num += 1

    print happies
    
