"""
Count Vowels - Enter a string and the program counts
the number of vowels in the text. For added complexity
have it report a sum of each vowel found.
"""

from collections import defaultdict

if __name__ == '__main__':
    string = raw_input('Enter a string: ').lower()

    vowels = ['a', 'e', 'i', 'o', 'u']
    counts = defaultdict(int)

    for char in string:
        if char in vowels:
            counts[char] += 1

    print counts.items()
