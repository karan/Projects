def _factorize(n):
    i = 2
    a = []
    n = int(n)
    s = n
    while n != 1:
        if n % i == 0:
            a.append(i)
            n = n / i
        else:
            i += 1

    if len(a) == 1 and a[0] == n:
        string = str(n) + " is a Prime Number"
    else:
        c = 1
        string = "The Prime Factorized Numbers of " + str(s) + " are: "
        while c < len(a):
            string += str(a[c-1])
            if c != len(a)-1:
                string += ", "
            c += 1
    return string


def shell():
    print("This piece of software shows the prime numbers")

    while True:
        print('>>> ', end='')
        entry = input()
        if entry == "quit" or entry == "q":
            break
        if not entry.isdigit():
            print("Thats not a Number. Please try again")
        else:
            print(_factorize(entry))


if __name__ == '__main__':
    shell()
