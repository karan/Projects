primes = [2]
num = 3

while len(primes) < 10001:
    for i in primes:
        if num % i == 0:
            break
    else: # part of for loop, executes if loop falls through (no break is executed)
        primes.append(num)
    num += 2 # small optimization

print primes[-1]