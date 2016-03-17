import math

##Enter a number and have the program generate PI up to that many decimal places. Keep a limit to how far the program will go.
#a = input('enter a number')
def finde(numb):
    mye = math.e # assign math.e to mypi
    return (round(mye, numb))

thee = finde(5)
print(thee)
