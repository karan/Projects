from number_to_word import numTrans

total = 0
for i in range(1,1001):
    total += len(filter(lambda a: a != " ", numTrans(i, style="UK")))
print total
