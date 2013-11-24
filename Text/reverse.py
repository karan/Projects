# -*- coding: cp1252 -*-
"""
Reverse a String - Enter a string and the program
will reverse it and print it out.
"""

string = raw_input("Whatchu wanna say to me? ")
copy = [c for c in string]
for i in range(len(copy) / 2):
    copy[i], copy[len(copy) - i - 1] = copy[len(copy) - i - 1], copy[i]
print "You say %s, I say %s" % (string, ''.join(copy))
