largest = 0
for i in range(1000, 0, -1):
    for j in range(1000, i, -1):
        num = str(i*j)
        if num == num[::-1] and i*j > largest:
            largest = i*j
        elif i*j <= largest:
            break

print largest