# Find PI to the Nth Digit

from __future__ import division


digits = raw_input("Enter number of digits to round PI to: ")
digits = int(digits)

# n-th term is < 10^-(2*n + 1)
# so n iterations gives you 2*n digits
iterations = digits//2 + 2

# pi = 4*(4*atan(1/5) - atan(1/239))
# atan(x) = sum(x=0..+inf, (-1)^n / (2*n + 1))
pi = 0

for n in xrange(iterations):
    pi += 4 * (4 * (-1)**n/(2*n + 1) * (1/5)**(2*n + 1) - (-1)**n/(2*n + 1) * (1/239)**(2*n + 1))

print("{{:.{}}}".format(digits + 1).format(pi))
