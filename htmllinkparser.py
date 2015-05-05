#!/usr/bin/env python

import HTMLParser, urlparse

class HTMLLinkFinder(HTMLParser.HTMLParser):
    def __init__(self, url):
        HTMLParser.HTMLParser.__init__(self)
        self.links = []
        self.url = url

    def handle_starttag(self, tag, attrs):
        if(tag == "a"):
            for attr in attrs:
                if(attr[0] == "href"):
                    link = attr[1].strip("//")
                    self.links.append(urlparse.urljoin(self.url, link))
