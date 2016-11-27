def eratosthenes(n):
	A = [True for i in range(2,n)]
	for i in range(2,int(n**0.5)+1):
		if A[i]:
			for j in range(i**2,n,i):
				A[j-2] = False
	return [i+2 for i, v in enumerate(A) if v]
print eratosthenes(500)