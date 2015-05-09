from creepyhtmlparser import CreepyHTMLParser

crawlledLinks = []

def crawl(page):
    global crawlledLinks

    print "Crawlled links:", crawlledLinks

    c = CreepyHTMLParser(page)
    parsed = c.parsePage()

    if not(parsed):
        return

    print page, ":", parsed, "\n"

    for link in parsed["links"]:
        if not(link.strip() in crawlledLinks):
            crawlledLinks.append(link.strip())
            crawl(link)

if __name__=="__main__":
    crawl("http://ebay.co.uk")
