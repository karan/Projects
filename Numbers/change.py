# Change Return Program - The user enters a cost and
# then the amount of money given. The program will figure
# out the change and the number of quarters, dimes, nickels,
# pennies needed for the change.

if __name__ == '__main__':
    cost = input("What's the cost in dollars? ")
    given = input("What's the amount of dollars given? ")

    change = given - cost

    print "\n"
    if change < 0:
        print "Please ask for $%.2f more from the customer." % (-change) # double negation
    else:
        print "The change is $%.2f." % change

        q = 0 # 0.25
        d = 0 # 0.10
        n = 0 # 0.05
        p = 0 # 0.01

        change = int(change * 100) # let's talk about cents
        
        if change >= 25:
            q = int(change / 25)
            change = change % 25
        if change >= 10:
            d = int(change / 10)
            change = change % 10
        if change >= 5:
            n = int(change / 5)
            change = change % 5
        if change >= 1:
            p = change # rest all change is in pennies

    print "Give the following change to the customer:"
    print "Quarters: %d\tDimes: %d\tNickels: %d\tPennies: %d" \
          % (q, d, n, p)

    # DEBUG
    # print "Total change per the number of coins is %.2f" % \
    #       ((q * .25) + (d * .10) + (n * 0.05) + (p * 0.01))
