from math import pi

##Enter a number and have the program generate PI up to that many decimal places. Keep a limit to how far the program will go.
def findpi(numb):
    mypi = pi # assign pi to mypi
    return (round(mypi, numb))

#a = raw_input('enter a number: ')
a = 4
thepi = findpi(a)
print(thepi)
