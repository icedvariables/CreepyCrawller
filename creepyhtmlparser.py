import HTMLParser, urlparse, urllib2, re, sys

class CreepyHTMLParser(HTMLParser.HTMLParser):
    def __init__(self, url):
        HTMLParser.HTMLParser.__init__(self)
        self.HEADER_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")
        self.RE_EMAIL = re.compile(r"[a-zA-Z\._]+@\w+\.\w+(\.\w+)?")

        self.url = url
        self.domain = urlparse.urlparse(url).netloc

        self.title = url
        self.description = ""
        self.keywords = []
        self.links = []
        self.images = []
        self.headers = []
        self.emails = []

        self._title = False
        self._header = False

    def parsePage(self):
        """Find links, images, emails, etc on a webpage"""

        raw = self.getPage(self.url)

        if(isinstance(raw, urllib2.URLError)):
            print "Failed to get page:", self.url, "error:", raw
            return

        try:
            self.feed(raw)
        except (UnicodeDecodeError, TypeError), e:
            print e

        self.emails += self.findEmails(raw)

        # Remove empty headers
        self.headers = filter(None, self.headers)

        return {"title":self.title, "description":self.description, "keywords":self.keywords, "links":self.links, "images":self.images, "headers":self.headers, "emails":self.emails}

    def getPage(self, url):
        """Fetch a page over HTTP"""

        try:
            page = urllib2.urlopen(url)
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

        if(tag == "title"):
            self._title = True

        if(tag == "meta"):
            content = ""
            for attr in attrs:
                if(attr[0] == "content"):
                    content = attr[1]

            for attr in attrs:
                if(attr[0] == "name"):
                    if(attr[1].lower() == "description"):
                        self.description = content
                    if(attr[1].lower() == "keywords"):
                        self.keywords = content.split(",")


        if(tag in self.HEADER_TAGS):
            self._header = True

    def handle_endtag(self, tag):
        if(tag in self.HEADER_TAGS):
            self._header = False

        if(tag == "title"):
            self._title = False

    def handle_data(self, data):
        if(self._header):
            self.headers.append(data.strip())

        if(self._title):
            self.title = data

    def makeAbsolute(self, url):
        """Make a url absolute ('/foo/bar' on 'site.com' would become 'site.com/foo/bar')"""

        link = urlparse.urlparse(url)
        if not(link.scheme):
            link = link._replace(scheme="http")
        if not(link.netloc):
            link = link._replace(netloc=self.domain)

        url = link.geturl()

        # just in case the urlparse method doesn't work
        if(url.startswith("http://http")):
            url = url[7:]

        # Remove self-links
        url = url.split("#")[0]

        return url

    def findEmails(self, data):
        """Returns an array of email address in data"""

        if(data):
            emails = []
            for email in self.RE_EMAIL.finditer(data):
                emails.append(email.group(0).strip())
            return emails

        return []


if __name__=="__main__":
    if(len(sys.argv) > 1):
        c = CreepyHTMLParser(sys.argv[1])
    else:
        print "Please specify a page to start crawlling on"
    print c.parsePage()
