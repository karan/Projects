vowels = ['a','e','i','o','u']

def pigLatin(text):
	parts = text.split()
	new_text = ''
	for word in parts:
		if word.isalpha():
			new_word = ''
			for char in word:
				if char not in vowels:
					pass
				else:
					index = word.find(char)
					new_word = word[index:] + word[0:index] + "ay"
			new_text = new_text + new_word + ' '
		else:
			new_text.rstrip()
			new_text += word
	return new_text

translate = pigLatin('This is a test; a test of the new system.')
print(translate)