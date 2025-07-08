import feedparser

feed = feedparser.parse("https://feeds.bbci.co.uk/news/rss.xml")
for entry in feed.entries[:5]:
    print(entry.title)
    print(entry.link)
