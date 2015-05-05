##!/usr/bin/env python

import urllib2, threading
import htmllinkparser

class Crawl():
    def __init__(self, site):
        self.site = site
        self.index = site.split("/")[0]
        self.indexLinks = self.findLinks(self.index)

    def findLinks(self, page):
        raw = self.getPage(page)

        parser = htmllinkparser.HTMLLinkFinder(self.site)
        try:
            parser.feed(raw)
        except UnicodeDecodeError, e:
            print "Invalid characters:", e
        return parser.links

    def getPage(self, url):
        page = urllib2.urlopen("http://" + url)
        data = page.read()
        return data

if __name__=="__main__":
    c = Crawl("stackoverflow.com/")
    print c.indexLinks
