def shell():
    print("This piece of software shows Pi to a user definded decimal.")

    while True:
        print('>>> ', end='')
        entry = input()
        if entry == "quit":
            break
        if not entry.isdigit():
            print("Thats not a Number. Please try again")
        else:
            print(entry)

if __name__=='__main__':
    shell()