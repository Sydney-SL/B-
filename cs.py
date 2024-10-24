import requests
import pandas as pd
from tkinter import *
from tkinter import filedialog
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def fetch_data(uid, max_per_page=500):
    base_url = "https://api.aicu.cc/api/v3/search/getreply"
    all_replies = []
    page_number = 1

    while True:
        # 发送请求
        response = requests.get(base_url, params={
            'uid': uid,
            'pn': page_number,
            'ps': max_per_page,
            'mode': 0
        })

        # 检查响应状态
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            break

        data = response.json()

        # 检查返回数据是否正确
        if data.get('code') != 0:
            print(f"错误代码: {data.get('code')}")
            break

        # 获取回复数据
        replies = data['data']['replies']
        all_replies.extend(replies)

        # 检查是否为最后一页
        if data['data']['cursor']['is_end']:
            break

        page_number += 1

    return all_replies

def save_to_excel(replies, uid, folder_path):
    # 将数据转换为 DataFrame
    df = pd.DataFrame(replies)

    # 生成文件路径和名称
    file_name = f"{uid}_评论数据.xlsx"
    file_path = folder_path + "\\" + file_name

    # 将 DataFrame 保存为 Excel
    df.to_excel(file_path, index=False)
    print(f"数据已保存到 {file_path}")

def generate_word_cloud(file_path):
    # 1. 从 Excel 中导入数据
    df = pd.read_excel(file_path)

    # 2. 数据处理（这里假设数据在 Excel 中的列名为 'message'）
    text = ' '.join(df['message'])  # 将所有文本拼接成一个长字符串

    # 3. 生成词云
    wordcloud = WordCloud(width=1920, height=1080, background_color='white', font_path='ip.ttf').generate(text)
    # ip.ttf是字体文件，放在同目录下
    # 4. 显示词云
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()

def start_program():
    # 获取用户输入的 UID
    uid = uid_entry.get()

    # 获取保存路径
    folder_path = filedialog.askdirectory()

    # 获取评论数据
    replies = fetch_data(uid)

    # 保存评论数据到 Excel
    save_to_excel(replies, uid, folder_path)

    # 生成词云
    file_path = folder_path + "\\" + f"{uid}_评论数据.xlsx"
    generate_word_cloud(file_path)

root = Tk()
root.title("B站视奸小助手")
root.geometry("400x200")  # 设置界面大小

# 创建 UID 输入框和标签
uid_label = Label(root, text="UID:")
uid_label.pack()
uid_entry = Entry(root)
uid_entry.pack()

# 创建开始按钮
start_button = Button(root, text="开始", command=start_program)
start_button.pack()

root.mainloop()
