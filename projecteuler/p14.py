maxi = 0
answ = 0
for b in range(1000000):
    times = 0
    a = b
    while not a == 1:
        a = a/2 if a % 2 == 0 else 3*a + 1
        times += 1
    if times > maxi:
        answ = a
        maxi = times