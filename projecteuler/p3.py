num = 600851475143

sieve = int(num**(1.0/2)) * [True] # create sieve
sieve[0] = False

for i in range(len(sieve)):
    if sieve[i]: # find next prime
        k = i + i + 1
        while k < len(sieve): # set multiples of primes to nonprime
            sieve[k] = False
            k += i + 1

primes = [i+1 for i in range(len(sieve)) if sieve[i]] # print index+1s of True's

for i in primes:
    while num % i == 0:
        num /= i
    if num == 1:
        print i
        break