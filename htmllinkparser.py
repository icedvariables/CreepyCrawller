#!/usr/bin/env python

import HTMLParser

class HTMLLinkFinder(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if(tag == "a"):
            for attr in attrs:
                if(attr[0] == "href"):
                    self.links.append(attr[1])
