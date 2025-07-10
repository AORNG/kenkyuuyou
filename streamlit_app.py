import streamlit as st
import feedparser
from newspaper import Article

st.title("BBC News RSS Feed with Article Content")

feed = feedparser.parse("https://feeds.bbci.co.uk/news/rss.xml")

for entry in feed.entries[:5]:
    st.subheader(entry.title)
    st.write(f"[Read original article]({entry.link})")

    try:
        # 記事の本文を取得
        article = Article(entry.link)
        article.download()
        article.parse()
        st.write(article.text[:500] + "…")  # 長いので最初の500文字だけ表示
    except Exception as e:
        st.warning(f"Failed to extract article content: {e}")
