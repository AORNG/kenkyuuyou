import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import requests
from datetime import date
import plotly.express as px
a="7限"
b="1221"
c="Thursday"

#ページ設定
st.set_page_config(
   page_title="教員用",
   layout="wide",
)

#excelデータ読み込み
df = pd.read_excel("./日課表.xlsx", sheet_name="Sheet1", header=0, usecols="A:F")

#データの修正
df = df.dropna()  # 空白データがある行を除外
df[["単価", "数量", "金額"]] = df[["単価", "数量", "金額"]].astype(int)  # 金額や数量を整数型に変換
df["月"] = df["購入日"].dt.month.astype(str)  # "月"の列を追加
df["購入日|部署"] = df["購入日"].astype(str).str.cat(df["部署"], sep="|")  # "購入日|部署" 列を追加

# 現在の年月を取得
today = date.today()  # 今日の日付を取得
this_year = today.year  # 年を取り出し
this_month = today.month  # 月を取り出し

# タイトル表示
st.title(f"{this_year}年{this_month}月")

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


# パスワードの保存
conn = sqlite3.connect("database.db")
c = conn.cursor()

# パスワードのハッシュ化
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return True
    return False

# ユーザー登録
def create_user():
    c.execute("CREATE TABLE IF NOT EXISTS usertable(username TEXT, password TEXT)")

# ユーザー追加
def add_user(username, password):
    c.execute("INSERT INTO usertable(username, password) VALUES (?, ?)", (username, password))
    conn.commit()

# ログイン
def login_user(username, password):
    c.execute("SELECT * FROM usertable WHERE username = ?", (username,))
    data = c.fetchall()
    if data:
        stored_hash = data[0][1]  # データベースに保存されているハッシュ
        if check_hashes(password, stored_hash):
            return True
    return False

# 画面作成
def main():
    st.title("教員用")

    menu = ["ホーム", "ログイン", "サインアップ"]
    choice = st.sidebar.selectbox("メニュー", menu)

    if choice == "ホーム":
        st.subheader("ホーム画面")
        check=st.text_input("入力")
        check_button=st.button("ボタン")
        if check_button:
            send_post_request('https://prod-01.japaneast.logic.azure.com:443/workflows/38f7b8c8d476411d8d4351e0638c6750/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=DQl_g5amg0IRCFIs1lRiIBvicQ1Z9JI9i7uNgWKKu2g', check)

    elif choice == "ログイン":
        username = st.sidebar.text_input("ユーザー名を入力")
        password = st.sidebar.text_input("パスワードを入力", type="password")
        if st.sidebar.checkbox("ログイン"):
            create_user()
            if login_user(username, password):
                st.success(f"{username}さんでログインしました")
            else:
                st.warning("ユーザー名かパスワードが間違っています")

    elif choice == "サインアップ":
        st.subheader("新しいアカウントを作成")
        new_user = st.text_input("ユーザー名を入力")
        new_password = st.text_input("パスワードを入力", type="password")

        if st.button("サインアップ"):
            create_user()
            add_user(new_user, make_hashes(new_password))
            st.success("アカウントの作成が完了しました")
            st.info("ログイン画面からログインしてください")

    # データベース接続を閉じる
    conn.close()

if __name__ == "__main__":
    main()
