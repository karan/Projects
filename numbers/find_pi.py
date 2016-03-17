from math import pi

##Enter a number and have the program generate PI up to that many decimal places. Keep a limit to how far the program will go.
def findpi(numb):
    mypi = pi # assign pi to mypi
    return (round(mypi, numb))

a = int(input('enter a number: '))

thepi = findpi(a)
print(thepi)
