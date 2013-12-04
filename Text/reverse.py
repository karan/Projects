# -*- coding: cp1252, jamesintonation -*-
"""
Reverse a String - Enter a string and the program
will reverse it and print it out.
"""

string = raw_input("Whatchu wanna say to me? ")
print "You say %s, I say %s" % (string, string[::-1])

# Reversing a string is easier than transforming it into an array, reversing the array, and rejoining it.
# Just iterate over the string in reverse.
