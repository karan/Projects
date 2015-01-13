num = 10000

sieve = num * [True] # create sieve
sieve[0] = False

for i in range(len(sieve)):
    if sieve[i]: # find next prime
        k = i + i + 1
        while k < len(sieve): # set multiples of primes to nonprime
            sieve[k] = False
            k += i + 1

primes = [i+1 for i in range(len(sieve)) if sieve[i]] # print index+1s of True's

factors = [0] * len(primes)

for i in range(num, 1, -1):
    for j in range(len(primes)): # get number of times each prime divides into i
        f = 0
        while i % primes[j] == 0:
            f += 1
            i /= primes[j]
        if f > factors[j]:
            factors[j] = f # if the prime divides into i more than the current prime factorization of solution set
                           # that amount as the exponent

sol = 1
for i in range(len(factors)):
    sol *= primes[i] ** factors[i]

print sol