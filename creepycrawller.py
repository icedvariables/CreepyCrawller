##!/usr/bin/env python

import urllib2, threading, urlparse
import creepyhtmlparser

class Crawl():
    def __init__(self, url):
        self.url = url

    def parsePage(self):
        raw = self.getPage(self.url)

        parser = creepyhtmlparser.CreepyHTMLParser(self.url)
        try:
            parser.feed(raw)
        except (UnicodeDecodeError, TypeError), e:
            print e

        return {"links":parser.links, "images":parser.images, "headers":parser.headers}

    def getPage(self, url):
        try:
            u = url
            if not(urlparse.urlparse(u).scheme):
                u = "http://" + u
            page = urllib2.urlopen(u)
        except urllib2.URLError, e:
            return e

        data = page.read()
        return data

if __name__=="__main__":
    c = Crawl("google.com")
    print c.parsePage()
