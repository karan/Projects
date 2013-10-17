# Find PI to the Nth Digit

from math import *

digits = raw_input('Enter number of digits to round PI to: ')

# print ('{0:.%df}' % min(20, int(digits))).format(math.pi) # nested string formatting

# calculate pi using Machin-like Formula
print ('{0:.%df}' % min(30, int(digits))).format(4 * (4 * atan(1.0/5.0) - atan(1.0/239.0)))
