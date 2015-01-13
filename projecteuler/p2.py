a = 0
b = 1
total = 0

while b < 4000000:
    total += b if b % 2 == 0 else 0
    a, b = b, a+b # a = b, b = a+b

print total