# -*- coding: cp1252 -*-
"""
Page Scraper - Create an application which connects to a
site and pulls out all links, or images, and saves them to
a list. Optional: Organize the indexed content and don’t
allow duplicates. Have it put the results into an easily
searchable index file.
"""

import urllib2
from bs4 import BeautifulSoup


def print_list(stuff):
    print '\n'.join(stuff)
    print '\n====================\n'

if __name__ == '__main__':
    
    url = raw_input('Enter a URL: ')

    choice = input('What to scrape?\n1. Links\n2. Images\n3. Both\n')
    
    soup = BeautifulSoup(urllib2.urlopen(url).read())

    if choice == 1 or choice == 3:
        urls = [link.get('href') for link in soup.findAll('a')]
        print 'URLs:'
        print_list(urls)
    if choice == 2 or choice ==3:
        images = [image['src'] for image in soup.findAll("img")]
        print 'Images:'
        print_list(images)
