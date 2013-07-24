"""
Count Words in a String - Counts the number of individual
words in a string and display the top 5/10 most used words.
"""

from collections import defaultdict
import operator

if __name__ == '__main__':
    text = raw_input('Enter some text: \n')
    words = text.split() # very naive approach, split at space

    counts = defaultdict(int) # no need to check existence of a key

    # find count of each word
    for word in words:
        counts[word] += 1

    # sort the dict by the count of each word, returns a tuple (word, count)
    sorted_counts = sorted(counts.iteritems(), \
                           key=operator.itemgetter(1), \
                           reverse=True)

    # print top 5 words
    for (i, (word, count)) in enumerate(sorted_counts):
        if i < 5:
            print (word, count)
