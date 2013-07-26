"""
Count Vowels - Enter a string and the program counts
the number of vowels in the text. For added complexity
have it report a sum of each vowel found.
"""

string = raw_input('Enter a string: ').lower()

vowels = ['a', 'e', 'i', 'o', 'u']
counts = dict(zip(vowels, [0, 0, 0, 0, 0]))

for char in string:
    if char in vowels:
        counts[char] += 1

print counts
