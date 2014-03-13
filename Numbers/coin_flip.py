from random import randint

# Lists that we will use to keep track of coin flip results
heads = []
tails = []

def coin_flip(trys):
    while trys > 0:
        flip = randint(0,1)
        if flip == 0:
            print("Heads")
            heads.append(0)
            trys -= 1
        else:
            print("Tails")
            tails.append(1)
            trys -= 1

# Ask user how many times to run the program
trys = str(input("How many times would you like to flip a coin?"))

# Check for valid input
while trys.strip() == "" or trys.isalpha():
    print("Please enter a number")
    trys = str(input("How many times would you like to flip a coin?"))
else:
    trys = int(trys)
    coin_flip(trys)

print("Heads:", len(heads))
print("Tails:", len(tails))