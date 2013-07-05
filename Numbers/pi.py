# Find PI to the Nth Digit

import math

digits = raw_input('Enter number of digits to round PI to: ')

print ('{0:.%df}' % min(20, int(digits))).format(math.pi) # nested string formatting
