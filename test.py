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
] + [
    "红楼梦",
    "西游记",
    "水浒传",
    "三国演义",
    "道德经",
    "论语",
    "诗经",
    "春秋",
    "焦裕禄",
    "孔子",
    "李白",
    "杜甫",
    "王维",
    "苏轼",
    "白居易",
    "曹操",
    "刘备",
    "孙权",
    "诸葛亮",
    "周瑜",
    "司马懿",
    "曹丕",
    "李自成",
    "项羽",
    "刘邦",
    "秦始皇",
    "武则天",
    "杨贵妃",
    "唐伯虎",
    "李清照",
    "朱元璋",
    "明太祖",
    "郭沫若",
    "钱钟书",
    "林语堂",
    "鲁迅",
    "梁启超",
    "茅盾",
    "老舍",
    "徐志摩",
    "矛盾论",
    "黑洞",
    "量子力学",
    "DNA",
    "相对论",
    "人工智能",
    "基因编辑",
    "全息投影",
    "大规模并行计算",
    "无人机",
    "太空探索",
    "物理学",
    "化学",
    "生物学",
    "天文学",
    "心理学",
    "计算机科学",
    "数学",
    "古墓丽影",
    "魂斗罗",
    "马里奥",
    "最终幻想",
    "生活用品",
    "洗衣机",
    "电视机",
    "冰箱",
    "空调",
    "手机",
    "电脑",
    "打印机",
    "微波炉",
    "吹风机",
    "咖啡机",
    "电饭煲",
    "烤箱",
    "豆浆机",
    "榨汁机",
    "电动牙刷",
    "扫地机器人",
    "电动剃须刀",
    "电动车",
    "自行车",
    "相机",
    "手表",
    "钢笔",
    "文件夹",
    "雨伞",
    "钥匙",
    "眼镜",
    "背包",
    "钱包",
    "餐具",
    "电池",
    "灯泡",
    "台灯",
    "花瓶",
    "植物",
    "猫",
    "狗",
    "鱼",
    "鸟",
    "老虎",
    "狮子",
    "大象",
    "熊",
    "兔子",
    "松树",
    "樱花",
    "莲花",
    "草地",
    "玫瑰",
    "向日葵",
    "仙人掌",
    "水仙",
    "菊花",
    "桃树",
    "葡萄",
    "苹果",
    "橘子",
    "香蕉",
    "草莓",
    "西瓜",
    "菠萝",
    "柠檬",
    "樱桃",
    "蘑菇",
    "南瓜",
    "玉米",
    "番茄",
    "土豆",
    "胡萝卜",
    "白菜",
    "茄子",
    "黄瓜",
    "西红柿",
    "蚂蚁",
    "蜜蜂",
    "蝴蝶",
    "蜻蜓",
    "螃蟹",
    "海豚",
    "鲨鱼",
    "乌龟",
    "大熊猫",
    "袋鼠",
    "狐狸",
    "鹿",
    "猴子",
    "蛇",
    "鸭子",
    "孔雀",
    "企鹅",
    "章鱼",
    "海星",
    "珊瑚",
    "海龟",
    "海马",
    "鲸鱼",
    "鳄鱼",
    "鹰",
    "老鹰",
    "白鹭",
    "蜗牛",
    "苍蝇",
    "蝈蝈",
    "蟋蟀",
    "螳螂",
    "蟑螂",
    "蜘蛛",
    "蝎子",
    "蟾蜍",
    "青蛙",
    "蜥蜴",
    "鳄鱼",
    "考拉",
    "袋鼠",
    "树袋熊",
    "刺猬",
    "箭毒蛙",
    "鸭嘴兽",
    "犀牛",
    "河马",
    "狮子",
    "豹子",
    "长颈鹿",
    "大象",
    "斑马",
    "黑猩猩",
    "猩猩",
    "树懒",
    "猴子",
    "狒狒",
    "海豚",
    "鲨鱼",
    "鲸鱼",
    "海豹",
    "海狮",
    "海燕",
    "海鸥",
    "大雁",
    "燕子",
    "喜鹊",
    "乌鸦",
    "鹦鹉",
    "鸽子",
    "白鹭",
    "孔雀",
    "野鸭",
    "火鸡",
    "雄鹰",
    "蜜蜂",
    "蚂蚁",
    "蝴蝶",
    "蜻蜓",
    "螳螂",
    "蝗虫",
    "甲虫",
    "蟋蟀",
    "蟑螂",
    "蜘蛛",
    "蜈蚣",
    "蚯蚓",
    "蜗牛",
    "海星",
    "海胆",
    "海葵",
    "珊瑚",
    "海绵",
    "海龟",
    "海豚",
    "鲨鱼",
    "鳐鱼",
    "鲸鱼",
    "鲱鱼",
    "鲤鱼",
    "鳗鱼",
    "鲈鱼",
    "鲫鱼",
    "黄鳝",
    "河虾",
    "螃蟹",
    "龙虾",
    "牡蛎",
    "鲍鱼",
    "扇贝",
    "蛤蜊",
    "海参",
    "海胆",
    "海苔",
    "水母",
    "鹦鹉螺",
    "象拔蚌",
    "海螺",
    "海葵",
    "珊瑚",
    "海绵",
    "海龟",
    "海马",
    "鲨鱼",
    "鳐鱼",
    "鲸鱼",
    "鲱鱼",
    "鲤鱼",
    "鳗鱼",
    "鲈鱼",
    "鲫鱼",
    "黄鳝",
    "河虾",
    "螃蟹",
    "龙虾",
    "牡蛎",
    "鲍鱼",
    "扇贝",
    "蛤蜊",
    "海参",
    "海胆",
    "海苔",
    "水母",
    "鹦鹉螺",
    "象拔蚌",
    "海螺",
    "珊瑚",
    "海绵",
    "海龟",
    "海马",
    "鲨鱼",
    "鳐鱼",
    "鲸鱼",
    "鲱鱼",
    "鲤鱼",
    "鳗鱼",
    "鲈鱼",
    "鲫鱼",
    "黄鳝",
    "河虾",
    "螃蟹",
    "龙虾",
    "牡蛎",
    "鲍鱼",
    "扇贝",
    "蛤蜊",
    "海参",
    "海胆",
    "海苔",
    "水母",
    "鹦鹉螺",
    "象拔蚌",
    "海螺"
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
    st.markdown("> 来和*chatGLM*一起玩你说我猜吧~")
    views = {
        "我来说": render_describe,  # Read first for display default
        "我来猜": render_guess,
    }
    choice = st.radio("请选择角色", views.keys())
    render_func = views.get(choice)
    render_func()


def render_describe():
    if "random_answer" not in st.session_state:
        random_answer = get_random_answer()
        describe_times = 0
        st.session_state.random_answer = random_answer
        st.session_state.describe_times = describe_times
        print(processing("clear"))
        print(processing(
            "你知道你说我猜这种游戏吗？接下来我需要你扮演这个游戏中猜谜的一方，通过我提供的若干个短语来猜测我的谜底。你只需要输出一个词代表谜底，不需要任何冗余的语句。示例:我说一部讲述电脑黑客的电影，你说黑客帝国。明白了吗？"))
    else:
        random_answer = st.session_state.get("random_answer")
        describe_times = st.session_state.get("describe_times")
    st.text("请描述: " + random_answer)
    describe = st.text_area("在这里输入(使用回车隔开)")
    if st.button("提交"):
        guess = processing(describe)
        print(guess)
        if random_answer in guess:
            st.success("我的猜测是: "+random_answer)
        else:
            st.error("猜错了:"+guess[:20]+"...")

    if st.button("重新开始游戏"):
        st.session_state.pop("random_answer")
        st.experimental_rerun()


def render_guess():
    if "random_word" not in st.session_state:
        random_word = get_random_answer()
        guess_times = 0
        print(processing("clear"))
        describe = processing(
            "你知道你说我猜这种游戏吗?接下来我需要你扮演游戏中的主持人。每一轮游戏中，第一步我先给你一个谜底，第二步你为我生成5个描述它的短语。现在我的谜底是: " + random_word)
        print(describe)
        st.session_state.random_word = random_word
        st.session_state.guess_times = guess_times
        st.session_state.describe = describe
    else:
        random_word = st.session_state.get("random_word")
        guess_times = st.session_state.get("guess_times")
        describe = st.session_state.get("describe")
    st.write('请猜测')
    lines = describe.split('\n')
    if len(lines) <= 2:
        st.session_state.describe = processing(
            "你知道你说我猜这种游戏吗?接下来我需要你扮演游戏中的主持人。每一轮游戏中，第一步我先给你一个谜底，第二步你为我生成5个描述它的短语。现在我的谜底是: " + random_word)
        st.experimental_rerun()
    for line in lines:
        if '我' in line or '你' in line:
            continue
        if line == "":
            continue
        line = line.replace(random_word, "")
        st.write(line)
    guess = st.text_input("输入谜底")
    if st.button("提交"):
        if guess != "" and (random_word in guess or guess in random_word):
            st.success("恭喜你，猜对了！")
        else:
            st.error("猜错了！")
    if st.button("重新开始游戏"):
        st.session_state.pop("random_word")
        st.session_state.pop("describe")
        st.experimental_rerun()


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
