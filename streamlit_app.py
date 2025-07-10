# 必要なライブラリをインポート
import streamlit as st
import feedparser
from newspaper import Article

# アプリのタイトルを表示
st.title("BBC News RSS Feed with Article Content")

# RSSフィードを取得（BBCニュースの最新記事一覧）
feed = feedparser.parse("https://feeds.bbci.co.uk/news/rss.xml")

# 最初の5記事をループして表示
for entry in feed.entries[:5]:
    # 記事のタイトルを表示
    st.subheader(entry.title)

    # 元の記事へのリンクを表示
    st.write(f"[Read original article]({entry.link})")

    try:
        # newspaper3kを使って記事ページを取得
        article = Article(entry.link)
        article.download()  # 記事ページをダウンロード
        article.parse()     # 本文をパース（構造解析）

        # 記事本文の先頭500文字を表示（全文が長いため一部のみ）
        st.write(article.text[:500] + "…")

    except Exception as e:
        # 取得に失敗した場合の警告表示
        st.warning(f"Failed to extract article content: {e}")
