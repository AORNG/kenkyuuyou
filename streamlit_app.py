from newspaper import Article

url = "https://www.bbc.com/news/world-66204202"
article = Article(url)
article.download()
article.parse()

print(article.title)
print(article.text[:300])  # 本文の冒頭を表示
