import HTMLParser, urlparse, urllib2

class CreepyHTMLParser(HTMLParser.HTMLParser):
    def __init__(self, url):
        HTMLParser.HTMLParser.__init__(self)
        self.HEADER_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")
        self.url = url

        self.links = []
        self.images = []
        self.headers = []

        self._header = False

    def parsePage(self):
        raw = self.getPage(self.url)

        try:
            self.feed(raw)
        except (UnicodeDecodeError, TypeError), e:
            print e

        return {"links":self.links, "images":self.images, "headers":self.headers}

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

    def handle_starttag(self, tag, attrs):
        if(tag == "a"):
            for attr in attrs:
                if(attr[0] == "href"):
                    self.links.append(self.makeAbsolute(attr[1]))

        if(tag == "img"):
            for attr in attrs:
                if(attr[0] == "src"):
                    self.images.append(self.makeAbsolute(attr[1]))

        if(tag in self.HEADER_TAGS):
            self._header = True

    def handle_endtag(self, tag):
        if(tag in self.HEADER_TAGS):
            self._header = False

    def handle_data(self, data):
        if(self._header):
            self.headers.append(data)

    def makeAbsolute(self, url):
        link = urlparse.urlparse(url)
        if not(link.scheme):
            link = link._replace(scheme="http")
        if not(link.netloc):
            link = link._replace(netloc=self.url)

        return link.geturl()


if __name__=="__main__":
    c = CreepyHTMLParser("google.com")
    print c.parsePage()
