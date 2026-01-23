import random

secrect_number = random.randint(1,10) 
guess_count = 0
guess_limit = 3
while guess_count < guess_limit :
    guess = int(input("Enter Your Guess Number : "))
    guess_count +=1 
    if guess == secrect_number:
        print (" You Won The Game ")
        break
else:
    print(" Hey You Guess 3 Times.... ")
    print(" Try Next Time... ")
