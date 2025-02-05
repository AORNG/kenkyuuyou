import streamlit as st
import sqlite3

def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def check_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    data = c.fetchall()
    conn.close()
    return len(data) != 0

def main():
    st.sidebar.title("Authentication Demo")
    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.radio("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        # You can display whatever you want on the home page

    elif choice == "Login":
        st.subheader("Login Section")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')

        if st.sidebar.button("Login"):
            if check_user(username, password):
                st.success("Logged In as {}".format(username))
                task = st.selectbox("Task", ["Add Post", "Analytics", "Profiles"])
                if task == "Add Post":
                    st.subheader("Add Your Post")
                elif task == "Analytics":
                    st.subheader("Analytics")
                elif task == "Profiles":
                    st.subheader("User Profiles")
            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            add_user(new_user, new_password)
            st.success("You have successfully created an account.")
            st.info("Go to Login Menu to login")

if __name__ == "__main__":
    create_users_table()
    main()
