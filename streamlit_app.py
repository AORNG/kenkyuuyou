import streamlit as st
import pandas as pd
import sqlite3
import hashlib

#パスワードの保存
conn = sqlite3.connect("database.db")
c = conn.cursor()

#パスワードのハッシュ化import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import requests
from datetime import date
import plotly.express as px

#ページ設定
st.set_page_config(
   page_title="教員用",
   layout="wide",
)

#excelデータ読み込み
df = pd.read_excel("Z:\74回生\個人フォルダ\1年次\2組\1221\日課表.xlsx", sheet_name="1年1組" , header=0, usecols="A:F")

#データの修正
df = df.dropna()  # 空白データがある行を除外

st.dataframe(df)

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

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

#ユーザー登録
def create_user():
    c.execute("CREATE TABLE IF NOT EXISTS usertable(username TEXT,password TEXT)")

#ユーザー追加
def add_user(username,password):
    c.execute("INSERT INTO usertable(user,password) VALUES (?,?)",(username,password))
    conn.commit()

#ログイン
def login_user(username,password):
    c.execute("SELECT * FROM usertable WHERE username =? AND password = ?",(username,password))
    data = c.fetchall()
    return data

#画面作成
def main():
    st.title("教員用")

    menu = ["ホーム","ログイン","サインアップ"]
    choice = st.sidebar.selectbox("メニュー",menu)

    if choice == "ホーム":
        st.subheader("ホーム画面")

    elif choice == "ログイン":
        username = st.sidebar.text_input("ユーザー名を入力")
        password = st.sidebar.text_input("パスワードを入力",type="password")
        if st.sidebar.checkbox("ログイン"):
            create_user()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:
                st.success("{}さんでログインしました".format(username))
            
            else:
                st.warning("ユーザー名かパスワードが間違っています")
    elif choice == "サインアップ":
        st.subheader("新しいアカウントを作成")
        new_user = st.text_input("ユーザー名を入力")
        new_password = st.text_input("パスワードを入力",type="password")

        if st.button("サインアップ"):
            create_user()
            add_user(new_user,make_hashes(new_password))
            st.success("アカウントの作成しました")
            st.info("ログイン画面からログインしてください")
if __name__ == "__name__":
    main()