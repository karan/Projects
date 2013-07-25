# -*- coding: cp1252 -*-
# Fibonacci Sequence - Enter a number and have the
# program generate the Fibonacci sequence to that number
# or to the Nth number

n = int(raw_input('How many numbers do you need? '))
series = [1]

while len(series) < n:
    if len(series) == 1:
        series.append(1)
    else:
        series.append(series[-1] + series[-2])

print series
