def bubble(a):
	if len(a) < 2: return
	for i in range(0,len(a)):
		swapped = False
		for j in range(len(a)-1,i+1,-1):
			if a[j] < a[j-1]:
				a[j], a[j-1], swapped = a[j-1], a[j], True
		if not swapped: break