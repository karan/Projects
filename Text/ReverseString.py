def revString(name):
	new_name = ''
	for char in name[::-1]:
		new_name += char
	return new_name

test = revString("Sean")
print(test)