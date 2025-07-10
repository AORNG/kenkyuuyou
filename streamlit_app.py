import streamlit as st
import feedparser

st.title("BBC News RSS Feed")

feed = feedparser.parse("https://feeds.bbci.co.uk/news/rss.xml")

for entry in feed.entries[:5]:
    st.subheader(entry.title)
    st.write(entry.link)
