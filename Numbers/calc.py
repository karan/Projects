"""
Calculator - A simple calculator to do basic operators.
"""

if __name__ == '__main__':
    try:
        num1 = int(raw_input("Number 1: "))
        num2 = int(raw_input("Number 2: "))
    except:
        print 'Invalid input'
    else:
        op = raw_input("Operation (+, -, /, *): ")
        if op not in '+-/*':
            print "Invalid operator"
        else:
            if op == '+':
                res = num1 + num2
            elif op == '-':
                res = num1 - num2
            elif op == '/':
                res = num1 / num2
            elif op == '*':
                res = num1 * num2
            print "%d %s %d = %d" % (num1, op, num2, res)
