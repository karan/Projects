import re

def numTrans(num, style="US"):
    ''' Takes in a string num and translates it into words.
        1 becomes one, 2 becomes two, 100 becomes one hundred,
        123 becomes one hundred and twenty three. Hyphens
        are not included. Supports up to one hundred
        thousand. Returns a string. (UK/US Style) US omits ands '''
    
    numStr = str(num)
    numStr = re.sub(r"\D", "", numStr)
    trans = ""
    place = ""
    incr = 0
    incr1 = 0
    for i in numStr[::-1]:
        '''print trans #uncomment to debug
        print "-"
        print i
        print incr
        print incr1'''
        iInt = int(i)
        if incr % 3 == 0:
            if place == trans and not place == "":
                trans = trans[len(valuesTranslate(incr1 - 1)):]
            trans = valuesTranslate(incr1) + trans
            place = trans
            trans = onesTranslate(iInt) + trans
        if incr % 3 == 1:
            trans = tensTranslate(iInt) + trans
        if incr % 3 == 2:
            if incr1 == 0 and not trans == "" and style == "UK":
                trans = "and " + trans
            if not iInt == 0:
                trans = onesTranslate(iInt) + "hundred " + trans
            incr1 += 1
        incr += 1
        irNumbersW = ["ten one", "ten two", "ten three", "ten four", "ten five", "ten six", "ten seven", "ten eight", "ten nine"]
        irNumbersR = ["eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
        for n in range(len(irNumbersW)):
            trans =  trans.replace(irNumbersW[n], irNumbersR[n])
    trans = trans.strip()

    return trans            

def onesTranslate(digit):
    ''' Takes in an integer digit and returns the one's
        place translation. 1 becomes one, 2 becomes two.
        Returns a string.                                   '''
    
    if type(digit) == int:
        transList = ["", "one ", "two ", "three ", "four ", "five ", "six ", "seven ", "eight ", "nine "]
        return transList[digit]
    else:
        raise Exception(TypeError)

def tensTranslate(digit):
    ''' Takes in an integer digit and returns the ten's
        place translation. 1 becomes ten, 2 becomes twenty.
        Returns a string.                                   '''
    
    if type(digit) == int:
        transList = ["", "ten ", "twenty ", "thirty ", "forty ", "fifty ", "sixty ", "seventy ", "eighty ", "ninety "]
        return transList[digit]
    else:
        raise Exception(TypeError)

def valuesTranslate(incr):
    ''' Takes in an integer incr and returns the value
        place translation. 0 becomes "", 1 becomes
        and, 2 becomes thousand, 3 becomes million.
        Returns a string.                                   '''
    
    if type(incr) == int:
        transList = ["", "thousand ", "million ", "billion ", "trillion ", "quadrillion ", "quintillion ", "sextillion ", "septillion ", "octillion ", "nontillion ", "decillion "]
        return transList[incr]
    else:
        raise Exception(TypeError)
