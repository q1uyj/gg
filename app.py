import streamlit as st
import requests


def main() -> None:
    st.header(f"Guessing Game")
    views = {
        "describe": render_describe,  # Read first for display default
        "guess": render_guess,
        "About": render_about,
    }
    choice = st.sidebar.radio("Go To Page:", views.keys())
    render_func = views.get(choice)
    render_func()


def render_describe():
    '### describe'
    chat_input = st.text_area("input: 使用回车隔开")
    if st.button("Submit"):
        resp = ai_guess(chat_input)
        st.text(resp)


def render_guess():
    '### guess'
    answer = "猪"
    try:
        data = {
            "word": "猪"
        }
        response = requests.request(
            "POST", "http://127.0.0.1:8000/describe/", data=data
        )
        st.text(response.text)
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
    chat_input = st.text_area("input: 猜出当前词语")
    if st.button("Submit"):
        if answer == chat_input:
            st.text("正确")
        else:
            st.text("错误")


def render_about():
    st.header('About')


def ai_guess(content):
    try:
        desc = content.split('\n')
        data = {
            "type": "动物",
            "description": desc
        }
        print(data)
        response = requests.request(
            "POST", "http://127.0.0.1:8000/guess/", data=data)
        return response.text
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")


if __name__ == '__main__':
    main()
