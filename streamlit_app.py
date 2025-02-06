import streamlit as st
import pandas as pd
import sqlite3
import hashlib

#パスワードの保存
conn = sqlite3.connect("database.db")
c = conn.cursor()

#パスワードのハッシュ化
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
if __name__ == "__main__":
    main()