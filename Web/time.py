"""
Get Atomic Time from Internet Clock - This program will get
the true atomic time from an atomic time clock on the Internet.
Use any one of the atomic clocks returned by a simple Google search.
"""

import re
import urllib2


def main():
    url = 'http://time.is/just'
    content = urllib2.urlopen(url).read()
    pattern = re.compile('<div id="twd">(.*?)</div>')

    find_match = re.search(pattern, content)

    location_pat = re.compile('<h1 id="pL" class="w90 tr"><a href="/facts/\w+">(.*)</a></h1>')
    location_match = re.search(location_pat, content)
    
    print 'The time in %s is %s' % \
          (location_match.group(1), find_match.group(1))

if __name__ == '__main__':
    main()
