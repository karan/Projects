"""
Get Atomic Time from Internet Clock - This program will get
the true atomic time from an atomic time clock on the Internet.
Use any one of the atomic clocks returned by a simple Google search.
"""

import re
from urllib2 import urlopen


def main():
    url = 'http://time.is/just'
    content = urlopen(url).read()
    pattern = re.compile('<div id="twd">(.*)<span id="ampm" style="font-size:21px;line-height:21px">(AM|PM)</span></div>')

    find_match = re.search(pattern, content)

    location_pat = re.compile('<h1 id="pL" class="w90 tr"><a href="/facts/\w+">(.*)</a></h1>')
    location_match = re.search(location_pat, content)
    
    print 'The time in %s is %s %s' % \
          (location_match.group(1), find_match.group(1), find_match.group(2))

if __name__ == '__main__':
    main()
