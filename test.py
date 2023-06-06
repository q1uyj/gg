import streamlit as st
import requests
# -*- coding:utf-8 -*-
import logging
from random import randint
import random
import re
from typing import Callable
from wudao.api_request import getToken
from wudao.utils.sse_util import SSEClient

MODEL_REQUEST_URL = "https://maas.aminer.cn/api/paas/model/v1/open/engines/sse/chatGLM_ST/chatGLM_ST"

# 接口API KEY
API_KEY = "9b109dd7ce29458dbc8258fc205a3a66"
# 公钥
PUBLIC_KEY = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKcwe8Ip9ZU9gZma7Elp4wCwEgzyi/1ZqucU8IilkJMJbAjl/AMpt5aniQK5rJqFyde/VMFVl9OfyEDoAXgOkgUCAwEAAQ=="

# 能力类型
ability_type = "chatGLM"
# 引擎类型
engine_type = "chatGLM"

token_result = getToken(API_KEY, PUBLIC_KEY)

_FIELD_SEPARATOR = ":"

word_list = [
    "拿破仑",
    "亚历山大大帝",
    "达·芬奇",
    "爱因斯坦",
    "牛顿",
    "马克思",
    "列宁",
    "华盛顿",
    "曼德拉",
    "拜占庭",
    "秦始皇",
    "李世民",
    "蒙古",
    "罗马",
    "埃及",
    "希腊",
    "波斯",
    "巴黎圣母院",
    "剑桥大学",
    "清华大学",
    "哈佛大学",
    "自由女神像",
    "纳米比亚",
    "巴西",
    "秘鲁",
    "伦敦",
    "伊斯坦布尔",
    "塞维利亚",
    "夏威夷",
    "芝加哥",
    "火星",
    "木星",
    "太阳",
    "人类基因组计划",
    "相对论",
    "量子力学",
    "黑洞",
    "DNA",
    "遗传学",
    "太空探索",
    "太阳能电池",
    "望远镜",
    "电话",
    "电视",
    "计算机",
    "汽车",
    "冰箱",
    "洗衣机",
    "电吹风",
    "微波炉",
    "吸尘器",
    "剃须刀",
    "餐具",
    "钢笔",
    "自行车",
    "相机",
    "手表",
    "电视遥控器",
    "书",
    "钥匙",
    "猫",
    "狗",
    "大象",
    "熊猫",
    "老虎",
    "松树",
    "橡树",
    "玫瑰",
    "莲花",
    "草莓",
    "苹果",
    "橙子",
    "西瓜",
    "香蕉",
    "草",
    "玉米",
    "蜜蜂",
    "蝴蝶",
    "猫头鹰",
    "鱼",
    "鲸鱼",
    "海豚",
    "狮子",
    "狼",
    "蚂蚁",
    "蜘蛛",
    "蝙蝠",
    "蛇",
    "鸟",
    "蝉",
    "杜鹃",
    "孔雀",
    "金鱼",
    "鲨鱼",
    "海星",
    "珊瑚",
    "玫瑰花",
    "太阳花",
    "柳树",
    "仙人掌",
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


def processing(prompt):
    import requests
    import pprint
    if token_result and token_result["code"] == 200:
        token = token_result["data"]
        headers = {"Authorization": token}

        history = []
        print()
        # print("'clear' to clear history and 'history' to show history. Ctrl-C to exit")
        print(prompt)

        if prompt == "clear":
            history = []
            print("History Cleared.")
            return None
        elif prompt == "history":
            print_history(history)
            print()

        json = {
            "top_p": 0.7,
            "temperature": 0.5,
            "prompt": prompt,
            "requestTaskNo": randomTaskCode(),
            "history": history,
        }

        response = requests.post(
            MODEL_REQUEST_URL,
            headers=headers,
            json=json,
            stream=True,
        )
        client = SSEClient(response)
        print_diff = prepare_print_diff(
            lambda e: e.data, lambda e: pprint.pprint(e.__dict__))
        print('Response: ')
        msg = ""
        for event in client.events():
            if (event.data):
                event.data = punctuation_converse_auto(event.data)
            if (event.event == "add"):
                msg = print_diff(event)
            elif (event.event == "finish" or event.event == "interrupted"):
                msg = print_diff(event)
                print()
                history.extend([prompt, event.data])
                # print("output_length: \t", len(event.data))
                break
            elif (event.event == "error"):
                msg = print_diff(event)
                print()
            else:
                pprint.pprint(event.__dict__)
        print()
        return msg
    else:
        print("获取token失败，请检查 API_KEY 和 PUBLIC_KEY")
        return None


def get_random_answer():
    return random.choice(word_list)


def main() -> None:
    st.set_page_config(
        page_title="Guessing Game",
        initial_sidebar_state="expanded"
    )
    st.title(f"Guessing Game")
    views = {
        "describe": render_describe,  # Read first for display default
        "guess": render_guess,
    }
    choice = st.sidebar.radio("Go To Page:", views.keys())
    render_func = views.get(choice)
    render_func()


def render_describe():
    st.header('describe')
    if "random_answer" not in st.session_state:
        random_answer = get_random_answer()
        describe_times = 0
        st.session_state.random_answer = random_answer
        st.session_state.describe_times = describe_times
        print(processing("clear"))
        print(processing("你知道你说我猜这种游戏吗？"))
        print(processing(
            "接下来我需要你扮演这个游戏中猜谜的一方，通过我提供的若干个短语来猜测我的谜底。你只需要输出一个词代表谜底，不需要任何冗余的语句。示例:我说一部讲述电脑黑客的电影，你说黑客帝国。明白了吗？"))
    else:
        random_answer = st.session_state.get("random_answer")
        describe_times = st.session_state.get("describe_times")
    st.text("请描述: " + random_answer)
    describe = st.text_area("input: 使用回车隔开")
    if st.button("提交"):
        guess = processing(describe)
        if random_answer in guess:
            st.write("我的猜测是: "+random_answer)
        else:
            st.error(guess)

    if st.button("重新开始游戏"):
        st.session_state.pop("random_answer")
        st.experimental_rerun()


def render_guess():
    st.header('guess')
    if "random_word" not in st.session_state:
        random_word = get_random_answer()
        guess_times = 0
        st.session_state.random_word = random_word
        st.session_state.describe_times = guess_times
    else:
        random_word = st.session_state.get("random_word")
        guess_times = st.session_state.get("guess_times")
    st.write('请猜测')
    print(processing("clear"))
    describe = processing(
        "你知道你说我猜这种游戏吗?接下来我需要你扮演游戏中的主持人。每一轮游戏中，第一步我先给你一个谜底，第二步你为我生成若干个描述它的短语。现在我的谜底是: " + random_word + "。请继续。")
    print(describe)
    lines = describe.split('\n')
    for line in lines:
        if '我' in line or '你' in line:
            continue
        if line == "":
            continue
        line = line.replace(random_word, "")
        st.write(line)
    guess = st.text_input("输入谜底")
    if st.button("重新开始游戏"):
        st.session_state.pop("random_word")
        st.experimental_rerun()
    if st.button("提交"):
        if random_word in guess or guess in random_word:
            st.write("恭喜你，猜对了！")
            st.stop()
        else:
            st.error("猜错了！")
            st.stop()


def randomTaskCode():
    return "%019d" % randint(0, 10**19)


def punctuation_converse_auto(msg):
    punkts = [
        [",", "，"],
        ["!", "！"],
        [":", "："],
        [";", "；"],
        ["\?", "？"],
    ]
    for item in punkts:
        msg = re.sub(r"([\u4e00-\u9fff])%s" % item[0], r"\1%s" % item[1], msg)
        msg = re.sub(r"%s([\u4e00-\u9fff])" % item[0], r"%s\1" % item[1], msg)
    return msg


def prepare_print_diff(nextStr: Callable[[any], str], printError: Callable[[], None]):
    previous = ""

    def print_diff(input):
        nonlocal previous
        str = nextStr(input)
        if (not str.startswith(previous)):
            last_line_index = str.rfind("\n") + 1
            if (previous.startswith(str[0: last_line_index])):
                return ("\r%s" % str[last_line_index:])
            else:
                print()
                print(1, "[[previous][%s]]" % previous)
                printError(input)
        else:
            return (str[len(previous):])
        previous = str

    return print_diff


def print_history(history):
    is_request = True
    for history_item in history:
        print("Request:" if is_request else "Response:")
        print("\t", history_item)
        is_request = not is_request


if __name__ == '__main__':
    main()
