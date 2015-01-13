num = 1000000

sieve = num * [True] # create sieve
sieve[0] = False

for i in range(len(sieve)):
    if sieve[i]: # find next prime
        k = i + i + 1
        while k < len(sieve): # set multiples of primes to nonprime
            sieve[k] = False
            k += i + 1

primes = [i+1 for i in range(len(sieve)) if sieve[i]] # print index+1s of True's

on = 0
factors = 1
while factors <= 500:
    on += 1
    number = (on*(on+1))/2
    factors = 1
    for j in range(len(primes)): # get number of times each prime divides into i
        exp = 1
        while number % primes[j] == 0:
            exp += 1
            number /= primes[j]
        factors *= exp
        if number == 1:
            break
    else:
        print "Error!"

print (on*(on+1))/2