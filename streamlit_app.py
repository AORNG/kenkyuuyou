import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import requests
from datetime import date
import plotly.express as px

# ページ設定
st.set_page_config(
   page_title="教員用",
   layout="wide",
)

# Excelファイルのアップロード
uploaded_file = st.file_uploader("Excelファイルをアップロード", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, sheet_name="1年1組", header=0, usecols="A:F")
        df = df.dropna()  # 空白データがある行を除外
        st.dataframe(df)
    except Exception as e:
        st.error(f"Excel ファイルの読み込みに失敗しました: {e}")
else:
    st.info("ファイルをアップロードしてください。")

# データベース接続の作成
conn = sqlite3.connect("database.db")
c = conn.cursor()

# パスワードのハッシュ化
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

# ユーザー登録テーブルの作成
def create_user_table():
    c.execute("CREATE TABLE IF NOT EXISTS usertable(username TEXT, password TEXT)")
    conn.commit()

# ユーザー追加
def add_user(username, password):
    c.execute("INSERT INTO usertable(username, password) VALUES (?, ?)", (username, password))
    conn.commit()

# ユーザーが存在するかチェック
def user_exists(username):
    c.execute("SELECT * FROM usertable WHERE username = ?", (username,))
    return c.fetchone() is not None

# ログイン
def login_user(username, password):
    c.execute("SELECT * FROM usertable WHERE username = ?", (username,))
    data = c.fetchall()
    if data:
        stored_hash = data[0][1]  # データベースに保存されているハッシュ
        if check_hashes(password, stored_hash):
            return True
    return False

# POSTリクエスト送信
def send_post_request(url, data):
    try:
        # 送信するJSONのキーを "body" に変更
        response = requests.post(url, json={"body": data})
        if response.status_code == 200:
            st.write("成功: ", response.json())
        else:
            st.write(f"エラー: {response.status_code}, 詳細: {response.text}")
    except Exception as e:
        st.write(f"リクエストエラー: {e}")

# メイン画面
def main():
    st.title("教員用")

    menu = ["ホーム", "ログイン", "サインアップ"]
    choice = st.sidebar.selectbox("メニュー", menu)

    if choice == "ホーム":
        st.subheader("ホーム画面")
        check = st.text_input("入力")
        check_button = st.button("ボタン")
        if check_button:
            send_post_request(
                'https://prod-01.japaneast.logic.azure.com:443/workflows/38f7b8c8d476411d8d4351e0638c6750/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=
