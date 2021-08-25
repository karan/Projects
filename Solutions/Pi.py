import math

num = int(input('Enter the range: '))

#numbers greater than 15 will result in Invalid output after 15 digits
if num>15:
    print(f"{math.pi:.15f}")
else:
    print(f"{math.pi:.{num}f}")



