from creepyhtmlparser import CreepyHTMLParser

def crawl(page):
    c = CreepyHTMLParser(page)
    parsed = c.parsePage()

    if not(parsed):
        return

    print page, ":", parsed, "\n"

    for link in parsed["links"]:
        crawl(link)

if __name__=="__main__":
    crawl("http://www.dreamdawn.com/sh/")
