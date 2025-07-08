from newspaper import Article

urls = ["https://www.bbc.com/news/article1", "https://www.cnn.com/article2"]
texts = []
for url in urls:
    article = Article(url)
    article.download()
    article.parse()
    texts.append(article.text)
