import streamlit as st
import random

# 词库
word_list = [
    "阿甘正传",
    "泰坦尼克号",
    "星球大战",
    "少年派的奇幻漂流",
    "盗梦空间",
    "肖申克的救赎",
    "阿凡达",
    "教父",
    "指环王",
    "哈利·波特",
    "银河系漫游指南",
    "无间道",
    "黑客帝国",
    "阿拉丁",
    "发条橙",
    "心灵捕手",
    "傲慢与偏见",
    "西游记之大圣归来",
    "寻梦环游记",
    "超能陆战队",
    "当幸福来敲门",
    "狮子王",
    "飞屋环游记",
    "侏罗纪公园",
]


def start_game():
    random_word = random.choice(word_list)  # 随机选择一个词
    return random_word


def play_game(random_word, guess):
    if random_word == guess:
        return "成功"
    else:
        return "失败"


if "random_word" not in st.session_state:
    st.session_state.random_word = start_game()

st.title("猜词游戏")

st.write("随机词：", st.session_state.random_word)  # 显示随机词

guess = st.text_input("请输入你的猜测")

if st.button("提交"):
    result = play_game(st.session_state.random_word, guess)
    st.write(result)

if st.button("重新开始游戏"):
    st.session_state.pop("random_word")
    st.experimental_rerun()
