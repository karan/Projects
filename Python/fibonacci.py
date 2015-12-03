# Fibonacci Sequence Generation

def Fib(n):
    a = b = 1
    print a,
    print b,
    for i in range(2,n):
        b = a + b
        a = b - a
        print b,

def main():
    print("Enter the Fibonnaci number length")
    n=input()
    Fib(n)


if __name__ == '__main__':
    main()#fibonacci number
