# Next Prime Number - Have the program find prime
# numbers until the user chooses to stop asking for
# the next one.

def next_prime(current):
    next_prime = current + 1 # start checking for primes 1 number after the current one
    i = 2
    while next_prime > i: # check with numbers up to next_prime - 1
        if next_prime % i == 0: # if number is divisible
            next_prime += 1 # ready to check the next number
            i = 2 # reset i to check divisibility again from 2
        else:
            i += 1 # increment the divisor
    return next_prime

if __name__ == '__main__':
    current_prime = 2
    while True:
        response = raw_input('Do you want the next prime? (Y/N) ')

        if response.lower().startswith('y'):
            print current_prime
            current_prime = next_prime(current_prime)
        else:
            break
