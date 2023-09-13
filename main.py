import requests
from bs4 import BeautifulSoup
import random
import os
import re
import time
import urllib.parse
import tkinter as tk
from tkinter import ttk, messagebox, Scrollbar, Listbox
import json
import jsonpath
import threading
import requests
from bs4 import BeautifulSoup

def luogu():
    # 定义爬取的URL
    url = "https://www.luogu.org/problemlist/1"

    # 发送HTTP请求
    response = requests.get(url)

    # 使用BeautifulSoup解析HTML页面
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到题目列表的容器
    problem_list = soup.find('div', {'id': 'problem-list'})

    # 定义存储题目信息的列表
    problem_info = []

    # 遍历题目列表，获取每道题的信息
    for problem in problem_list.find_all('div', {'class': 'problem-item'}):
        title = problem.find('h2').text
        id = problem['data-id']
        link = "https://www.luogu.org/problem/" + id
        problem_info.append((title, link))

# 输出每道题的信息
    for i, problem in enumerate(problem_info):
        print(f"第{i+1}题: {problem[0]}")
        print(f"链接: {problem[1]}\n")

def test():
    # 定义爬取的网站地址

    url = "https://example.com"

    # 发送HTTP请求并获取响应内容

    response = requests.get(url)

    # 使用BeautifulSoup解析HTML内容

    soup = BeautifulSoup(response.text, "html.parser")

    # 在网页中查找题目信息并存储到列表中

    items = []

    for item in soup.find_all("div", class_="item"):
        items.append({

            "title": item.find("h2").text,

            "difficulty": item.find("span", class_="difficulty").text,

            "keywords": [keyword.text for keyword in item.find_all("span", class_="keyword")]

        })

        # 打印题目信息

    for item in items:
        print(item)

cookie = {
    'login_referer': 'https%3A%2F%2Fwww.luogu.com.cn%2Fproblem%2FP1000',
    '_uid': '111884',
    '__client_id': '4f1bbbf98da6e49a6c98727320089c851c18d53c',
    'C3VK': 'aa6e71',
}

global difficulty_var, source_options, keyword_entry, result_text, source_vars, database_info_label, source_listbox, progress_window, progress_label, progress_bar, text_output, progress_bar
original_window_size = "400x200"


def update_progress():
    progress_bar.step(1)  # 更新进度条的值
    progress_window.after(2, update_progress)  # 100毫秒后再次调用update_progress函数，实现循环滚动


def create_progress_window():
    global progress_window, progress_bar, text_output, progress_label
    progress_window = tk.Toplevel(root)
    progress_window.title("进度")
    progress_window.geometry("400x200")

    progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
    progress_bar.pack(pady=20)

    progress_label = tk.Label(progress_window, text="...")
    progress_label.pack()

    text_output = tk.Text(progress_window, wrap=tk.WORD)
    text_output.pack(fill=tk.BOTH, expand=True)

    progress_window.protocol("WM_DELETE_WINDOW", lambda: None)

    update_progress()



def close_progress_window():
    if progress_window and progress_window.winfo_exists():
        progress_window.destroy()


def Get_info(anum, bnum):
    headers = {
        "authority": "www.luogu.com.cn",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Cookie": "__client_id=a0306231cd05f9a814ca1bdf95c050400268bedf; _uid=0",
    }
    tag_url = 'https://www.luogu.com.cn/_lfe/tags'
    tag_html = requests.get(url=tag_url, headers=headers).json()
    tags_dicts = []
    tags_tag = list(jsonpath.jsonpath(tag_html, '$.tags')[0])
    for tag in tags_tag:
        if jsonpath.jsonpath(tag, '$.type')[0] != 1 or jsonpath.jsonpath(tag, '$.type')[0] != 4 or \
                jsonpath.jsonpath(tag, '$.type')[0] != 3:
            tags_dicts.append({'id': jsonpath.jsonpath(tag, '$.id')[0], 'name': jsonpath.jsonpath(tag, '$.name')[0]})

    arr = ['暂无评定', '入门', '普及−', '普及/提高−', '普及+/提高', '提高+/省选−', '省选/NOI−', 'NOI/NOI+/CTSC']
    ts = []
    # //是整除符号
    a = (anum - 1000) // 50 + 1
    b = (bnum - 1000) // 50 + 1

    for page in range(a, b + 1):
        # page = 1
        url = f'https://www.luogu.com.cn/problem/list?page={page}'
        html = requests.get(url=url, headers=headers).text
        urlParse = re.findall('decodeURIComponent\((.*?)\)\)', html)[0]
        htmlParse = json.loads(urllib.parse.unquote(urlParse)[1:-1])
        result = list(jsonpath.jsonpath(htmlParse, '$.currentData.problems.result')[0])

        for res in result:
            pid = jsonpath.jsonpath(res, '$.pid')[0]

            ppid = pid[1:]

            if int(ppid) < anum:
                continue

            if int(ppid) > bnum:
                break

            title = jsonpath.jsonpath(res, '$.title')[0]
            difficulty = arr[int(jsonpath.jsonpath(res, '$.difficulty')[0])]
            tags_s = list(jsonpath.jsonpath(res, '$.tags')[0])
            tags = []
            for ta in tags_s:
                for tags_dict in tags_dicts:
                    if tags_dict.get('id') == ta:
                        tags.append(tags_dict.get('name'))
            wen = {
                "题号": pid,
                "题目": title,
                "标签": tags,
                "难度": difficulty
            }
            ts.append(wen)
        print(f'第{page}页已保存')
        text_output.insert(tk.END, f'第{page}页已保存\n')
        text_output.see(tk.END)
        # 将数据写入JSON文件
        with open('info.json', 'w', encoding='utf-8') as f:
            json.dump(ts, f, ensure_ascii=False, indent=4)




def Get_TJ_MD(html):
    soup = BeautifulSoup(html, "html.parser")
    encoded_content_element = soup.find('script')
    encoded_content = encoded_content_element.text
    start = encoded_content.find('"')
    end = encoded_content.find('"', start + 1)
    encoded_content = encoded_content[start + 1:end]
    decoded_content = urllib.parse.unquote(encoded_content)
    decoded_content = decoded_content.encode('utf-8').decode('unicode_escape')
    start = decoded_content.find('"content":"')
    end = decoded_content.find('","type":"题解"')
    decoded_content = decoded_content[start + 11:end]

    return decoded_content


def Get_Problem_title(problemID):
    # 生成要访问的url
    url = 'https://www.luogu.com.cn/problem/P' + str(problemID)
    print('----------- 正在爬取 ' + str(problemID) + ' ------------')
    text_output.insert(tk.END, '----------- 正在爬取 ' + str(problemID) + ' ------------\n')
    text_output.see(tk.END)
    with open('user_agents.txt', 'r') as f:
        lines = f.readlines()
        custom_user_agent = random.choice(lines).strip()
    # 设置请求头
    headers = {
        'User-Agent': custom_user_agent,
    }
    # 创建请求
    r = requests.get(url, headers=headers)

    # 获取网页内容
    soup = BeautifulSoup(r.text, 'html.parser')

    # 获取题目标题
    title = soup.find('title').text
    # 将题目取到标题中-前的部分
    title = title.split('-')[0]
    # 将题目末尾空格去掉
    title = title.strip()

    # 结束函数
    return title


def start_work(anum, bnum):
    create_progress_window()

    print("正在爬取info...")
    text_output.insert(tk.END, "正在爬取info...\n")
    text_output.see(tk.END)
    Get_info(anum, bnum)
    print("info爬取成功！")
    text_output.insert(tk.END, "info爬取成功！\n")
    text_output.see(tk.END)  # 滚动到文本框底部显示新的消息
    bnum += 1
    for problemID in range(anum, bnum):

        time.sleep(random.randint(1, 3))

        url = 'https://www.luogu.com.cn/problem/P' + str(problemID)

        title = Get_Problem_title(problemID)
        # 打印提示信息
        print('题目标题：' + str(title))
        text_output.insert(tk.END, '题目标题：' + str(title) + '\n')
        text_output.see(tk.END)
        # 打印提示信息
        print('正在爬取题目...')
        text_output.insert(tk.END, '正在爬取题目...\n')
        text_output.see(tk.END)

        # 获取html
        # 从user_agents.txt里随机选择一行，作为本次请求的User-Agent
        with open('user_agents.txt', 'r') as f:
            lines = f.readlines()
            custom_user_agent = random.choice(lines).strip()
        # 设置请求头
        headers = {
            'User-Agent': custom_user_agent,
        }
        # 创建请求
        r = requests.get(url, headers=headers, cookies=cookie)
        # 获取网页内容
        html = r.text

        # 判断是否爬取成功
        if html == 'error':
            print('题目爬取失败！')
            text_output.insert(tk.END, '题目爬取失败！\n')
            text_output.see(tk.END)

        else:
            print('已获取题目网页源码！')
            text_output.insert(tk.END, '已获取题目网页源码！\n')
            text_output.see(tk.END)

            # 调用函数，传入html，获取题目MD文件
            problemMD = Get_MD(html)
            print("获取题目MD文件成功！")
            text_output.insert(tk.END, "获取题目MD文件成功！\n")
            text_output.see(tk.END)

            # 将题目编号-题目标题作为文件名
            filename = 'P' + str(problemID) + '-' + str(title) + '.md'
            # 在data目录下新建以题目编号-题目标题为名的文件夹
            # 判断文件夹是否存在
            if not os.path.exists('data/' + 'P' + str(problemID) + '-' + str(title)):
                os.mkdir('data/' + 'P' + str(problemID) + '-' + str(title))
                print('已创建文件夹：P' + str(problemID) + '-' + str(title))
                text_output.insert(tk.END, '已创建文件夹：P' + str(problemID) + '-' + str(title) + '\n')
                text_output.see(tk.END)
            else:
                print('文件夹已存在，无需创建！')
                text_output.insert(tk.END, '文件夹已存在，无需创建！\n')
                text_output.see(tk.END)
            # 将文件保存到data目录下
            with open('data/' + 'P' + str(problemID) + '-' + str(title) + '/' + filename, 'w', encoding='utf-8') as f:
                f.write(problemMD)
            # 打印提示信息
            print('题目爬取成功！')
            text_output.insert(tk.END, '题目爬取成功！\n')
            text_output.see(tk.END)

        # 开始爬取题解
        print("正在爬取题解...")
        text_output.insert(tk.END, "正在爬取题解...\n")
        text_output.see(tk.END)

        # 获取题解url
        url = 'https://www.luogu.com.cn/problem/solution/P' + str(problemID)

        # 创建请求
        r = requests.get(url, headers=headers, cookies=cookie)
        # 获取网页内容
        html = r.text
        # 判断是否爬取成功
        if html == 'error':
            print("题解爬取失败！")
            text_output.insert(tk.END, "题解爬取失败！\n")
            text_output.see(tk.END)
        else:
            print("已获取题解网页源码！")
            text_output.insert(tk.END, "已获取题解网页源码！\n")
            text_output.see(tk.END)

            # 调用函数，传入html，获取题解MD文件
            solutionMD = Get_TJ_MD(html)
            print("获取题解MD文件成功！")
            text_output.insert(tk.END, "获取题解MD文件成功！\n")
            text_output.see(tk.END)

            # 将题目编号-题目标题-题解作为文件名
            filename = 'P' + str(problemID) + '-' + str(title) + '-题解.md'
            # 将文件保存到data/problemID-title目录下
            # print(solutionMD)
            with open('data/' + 'P' + str(problemID) + '-' + str(title) + '/' + filename, 'w', encoding='utf-8') as f:
                f.write(solutionMD)

            # 打印提示信息
            print('题解爬取成功！')
            text_output.insert(tk.END, '题解爬取成功！\n')
            text_output.see(tk.END)

    # 更新数据库条数信息
    update_database_info()

    # 打印提示信息
    print('\n')
    print('所有题目爬取完毕！')
    text_output.insert(tk.END, '\n')
    text_output.see(tk.END)

    # 关闭进度条窗口
    close_progress_window()
    # 弹出提示框，并提示爬取成功题目的数量
    messagebox.showinfo(title='提示', message='所有题目爬取完毕！')


# 创建函数，用于切换页面
def show_frame(frame, window_size=None):
    frame.tkraise()

    if window_size:
        root.geometry(window_size)


def center_widgets(frame):

    def start_button_click():
        global progress_window
        left_range = left_range_entry.get()
        right_range = right_range_entry.get()
        try:
            left_range = int(left_range)
            right_range = int(right_range)
            if left_range < 1000 or 9635 < right_range < left_range:

                messagebox.showerror("错误", "题号范围无效，请输入1000-9634之间的题号，且开始题号不能大于结束题号")
                return
        except ValueError:

            messagebox.showerror("错误", "请输入有效的整数题号")
            return

        crawl_thread = threading.Thread(target=lambda: start_work(left_range, right_range))
        crawl_thread.start()

    inner_frame = tk.Frame(frame)
    inner_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # 在内部 Frame 上添加左范围输入框
    left_range_label = tk.Label(inner_frame, text="题号1:")
    left_range_label.grid(row=0, column=0, pady=9)
    left_range_entry = tk.Entry(inner_frame)
    left_range_entry.grid(row=0, column=1, pady=9)

    right_range_label = tk.Label(inner_frame, text="题号2:")
    right_range_label.grid(row=1, column=0, pady=9)
    right_range_entry = tk.Entry(inner_frame)
    right_range_entry.grid(row=1, column=1, pady=9)


    start_button = tk.Button(inner_frame, text="开始", command=start_button_click)
    start_button.grid(row=2, column=0, columnspan=2, pady=9)

    inner_frame.columnconfigure(0, weight=1)
    inner_frame.columnconfigure(1, weight=1)
    inner_frame.rowconfigure(0, weight=1)
    inner_frame.rowconfigure(1, weight=1)
    inner_frame.rowconfigure(2, weight=1)


def perform_search():
    global difficulty_var, source_options, keyword_entry, result_text, source_vars, source_listbox

    def load_problem_data():
        try:
            with open('info.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return []    # 在你的代码中调用这个函数来加载题目数据
    题目数据 = load_problem_data()

    # 获取用户选择的标签选项
    selected_tags_indices = source_listbox.curselection()
    selected_tags = [source_options[i] for i in selected_tags_indices]

    selected_difficulty = difficulty_var.get()
    keyword = keyword_entry.get().lower()


    result_text.delete(1.0, tk.END)


    found = False


    for 题目 in 题目数据:
        难度匹配 = selected_difficulty == "所有难度" or selected_difficulty == 题目["难度"]
        标签匹配 = not selected_tags or any(tag in selected_tags for tag in 题目["标签"])
        关键词匹配 = not keyword or keyword in 题目["题目"].lower() or any(
            keyword in tag.lower() for tag in 题目["标签"])

        if 难度匹配 and 标签匹配 and 关键词匹配:
            result_text.insert(tk.END,
                               f"题号：{题目['题号']}\n题目：{题目['题目']}\n难度：{题目['难度']}\n标签：{', '.join(题目['标签'])}\n\n")
            found = True
    if not found:
        messagebox.showinfo("未找到", "未找到匹配的题目。")
        # 清空选择
        difficulty_var.set("所有难度")
        source_listbox.selection_clear(0, tk.END)
        keyword_entry.delete(0, tk.END)


def get_tags_from_json():
    try:
        with open('info.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            tags_set = set()
            for item in data:
                tags_set.update(item['标签'])
            return list(tags_set)
    except FileNotFoundError:
        return []


def get_selected_tags():
    # 获取标签选项
    source_options = get_tags_from_json()
    selected_tags = [source_options[i] for i, var in enumerate(source_vars) if var.get()]
    return selected_tags



def build_page1():
    global database_info_label

    root.geometry("400x200")

    page1_frame = tk.Frame(container)
    page1_frame.grid(row=0, column=0, sticky="nsew")


    back_to_main_page1 = tk.Button(page1_frame, text="返回首页", command=return_to_main_page)
    back_to_main_page1.grid(row=0, column=0, pady=10)


    center_widgets(page1_frame)

    return page1_frame


def return_to_main_page():
    # 设置窗口的尺寸为默认尺寸
    root.geometry("400x200")
    show_frame(main_frame)


# 主函数，程序的开始
if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    # 使用python GUI
    root.title("洛谷爬虫")
    # 设置窗口大小
    root.geometry("650x350")

    # 设置窗口图标
    root.iconbitmap("png.jpg")

    # 创建一个容器，容器中装载的就是前端页面
    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    # 创建主页面
    main_frame = tk.Frame(container)
    main_frame.grid(row=0, column=0, sticky="nsew")

    # 添加标题标签
    title_label = tk.Label(main_frame, text="使用爬虫爬取题目", font=("Arial", 16), padx=10, pady=10)
    title_label.grid(row=0, column=0, columnspan=1)

    crawler_button = ttk.Button(main_frame, text="开始爬虫", command=lambda: show_frame(build_page1()))
    crawler_button.grid(row=1, column=0, pady=20)

    # 初始显示主页面
    show_frame(main_frame)

    # 运行主循环
    root.mainloop()