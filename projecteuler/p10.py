num = 2000000

sieve = num * [True] # create sieve
sieve[0] = False

for i in range(len(sieve)):
    if sieve[i]: # find next prime
        k = i + i + 1
        while k < len(sieve): # set multiples of primes to nonprime
            sieve[k] = False
            k += i + 1

primes = [i+1 for i in range(len(sieve)) if sieve[i]] # print index+1s of True's

print sum(primes)