import math

def shell():
    print("This piece of software shows Pi to a user definded decimal. (max 15)")

    while True:
        print('>>> ', end='')
        entry = input()
        if entry == "quit" or entry == "q":
            break
        if not entry.isdigit():
            print("Thats not a Number. Please try again")
        else:
            if int(entry) <= 15:
                print(str(math.pi)[0:int(entry)+2])#
            else:
                print(math.pi, "| 15 is the max of after decimals")

if __name__=='__main__':
    shell()