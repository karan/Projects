def fizzBuzz(n = 100):
	for i in range(n + 1):
		if (i % 3 == 0) & (i % 5 == 0):
			print("FizzBuzz")
		elif (i % 3 == 0):
			print("Fizz")
		elif (i % 5 == 0):
			print("Buzz")
		else:
			print(i)

if __name__ == "__main__":
	fizzBuzz()
