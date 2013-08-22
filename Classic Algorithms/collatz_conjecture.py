"""
Collatz Conjecture
Start with a number n > 1. Find the number of steps it
takes to reach one using the following process: If n is
even, divide it by 2. If n is odd, multiply it by 3 and
add 1.
"""


class Collatz:

    def __init__(self, number):
        self.number = number
        self.steps = 0

    def calculate_steps(self):
        while (self.number > 1):
            if self.number % 2 is 0:
                print '%d is even' % self.number
                self.number = self.number / 2
            else:
                print '%d is odd' % self.number
                self.number = self.number * 3 + 1
            self.steps += 1
            print '%d is the new number' % self.number

    def get_steps(self):
        print '*' * 50
        print '%d steps were taken to reach 1' % self.steps
        print '*' * 50

if __name__ == '__main__':
    number1 = Collatz(5)
    number1.calculate_steps()
    number1.get_steps()

    number2 = Collatz(10)
    number2.calculate_steps()
    number2.get_steps()

    number3 = Collatz(6)
    number3.calculate_steps()
    number3.get_steps()
