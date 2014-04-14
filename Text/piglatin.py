"""
Pig Latin - Pig Latin is a game of alterations played
on the English language game. To create the Pig Latin
form of an English word the initial consonant sound is
transposed to the end of the word and an ay is affixed
(Ex.: "banana" would yield anana-bay). Read Wikipedia
for more information on rules.
"""

word = raw_input('What\'s your word? ').lower()
vowels = 'aeiou'

pig = 'ay'

consonant = []
count = 0
copy = [c for c in word]

for i in range(len(copy) - 1):
	count = i
	if copy[i] in vowels:
		break
	else:
		consonant.append(copy[i])
		
new = word[count:] + "".join(consonant) + pig

"""
first = word[0]

if first in vowels:
    new = word + pig
else:
    new = word[1:] + first + pig
"""

print new
