"""
RSS Feed Creator - Given a link to RSS/Atom Feed,
get all posts and display them.
"""

import re
import urllib2


def main():
    """
    Takes in a Feedburned feed URL.

    Eg: http://feeds.feedburner.com/WebDesignLedger
    """
    feed_url = raw_input('Enter Feedburner RSS URL: ')
    content = urllib2.urlopen(feed_url).read() # get the source code of feed

    link_pattern = re.compile('<link>(.*)</link>')
    title_pattern = re.compile('<title>(.*)</title>')

    links = re.findall(link_pattern, content)[1:] # skip blog url
    titles = re.findall(title_pattern, content)[1:] # skip the page title

    for (link, title) in zip(links, titles):
        print '{0}\n{1}\n'.format(title, link)

if __name__ == '__main__':
    main()
