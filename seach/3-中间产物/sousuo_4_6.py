import tkinter as tk
from tkinter import filedialog
import pandas as pd
import re

# 创建窗口
root = tk.Tk()
root.withdraw()

# 选择日志文件
log_file_path = filedialog.askopenfilename(title='选择日志文件', filetypes=[('日志文件', '*.txt')])

# 选择规则文件
rules_file_path = filedialog.askopenfilename(title='选择规则文件', filetypes=[('Excel文件', '*.xlsx')])

# 读取规则文件
df = pd.read_excel(rules_file_path)

# 创建输出窗口
output_window = tk.Tk()
output_window.title('匹配结果')

# 获取屏幕的宽度和高度
screen_width = output_window.winfo_screenwidth()
screen_height = output_window.winfo_screenheight()

# 设置输出窗口的大小和位置
output_width = int(screen_width * 0.8)  # 输出窗口宽度为屏幕宽度的80%
output_height = int(screen_height * 0.8)  # 输出窗口高度为屏幕高度的80%
output_x = int((screen_width - output_width) / 2)  # 输出窗口的x坐标为屏幕中心
output_y = int((screen_height - output_height) / 2)  # 输出窗口的y坐标为屏幕中心
output_window.geometry(f"{output_width}x{output_height}+{output_x}+{output_y}")

# 创建输出框
output_frame = tk.Frame(output_window)
output_frame.pack(fill=tk.BOTH, expand=True)

# 设置Grid布局的行和列
output_frame.rowconfigure(0, weight=1)
output_frame.columnconfigure(0, weight=1)

# 遍历每一行规则
for index, row in df.iterrows():
    pattern = row['规则']  # 获取规则
    result = row['结果']   # 获取结果

    # 创建一个Frame，用于存储匹配结果
    rule_frame = tk.Frame(output_frame, relief=tk.RIDGE, bd=2)
    rule_frame.grid(row=index, column=0, sticky=tk.NSEW)

    # 创建一个Button，用于展开或折叠该规则的输出
    button_text = tk.StringVar()
    button_text.set("展开")
    button = tk.Button(rule_frame, textvariable=button_text, command=lambda frame=rule_frame, text=button_text: toggle_frame(frame, text))
    button.pack(side=tk.TOP, fill=tk.X)

    # 创建一个列表，用于存储匹配结果
    matches = []

    with open(log_file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if re.search(pattern, line):
                matches.append(f"Line {i}: {line.strip()}")  # 将匹配结果添加到列表中

    # 如果有匹配结果，则输出匹配结果
    if matches:
        # 创建一个Label，用于显示规则和结果
        label_text = f"规则：{pattern}\n结果：{result}\n"
        label = tk.Label(rule_frame, text=label_text, font=('Arial', 12), anchor=tk.W)
        label.pack(side=tk.TOP, fill=tk.X)

        # 创建一个Text，用于显示匹配项
        text = tk.Text(rule_frame, width=80, height=10, wrap=tk.WORD)
        text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        for match in matches:
            text.insert(tk.END, f"{match}\n")

        # 隐藏匹配项的Text
        text.grid_remove()

# 设置输出框的大小和其他属性
output_frame.config(width=output_width, height=output_height)

# 创建一个Button，用于展开或折叠规则窗口
toggle_button = tk.Button(output_window, text="规则", bg="#4CAF50", fg="white", font=('Arial', 12), command=lambda: toggle_frame(rules_frame, toggle_button))
toggle_button.place(relx=0.95, rely=0.95, anchor=tk.SE)

# 创建一个Frame，用于存储规则窗口
rules_frame = tk.Frame(output_window, relief=tk.RIDGE, bd=2)
rules_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# 创建一个Label，用于显示规则
rules_label = tk.Label(rules_frame, text="游戏规则", font=('Arial', 16), anchor=tk.W)
rules_label.pack(side=tk.TOP, fill=tk.X)

# 创建一个Text，用于显示游戏规则
rules_text = tk.Text(rules_frame, width=80, height=10, wrap=tk.WORD)
rules_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
rules_text.insert(tk.END, "1. 游戏开始后，每个玩家会随机获得一张牌。\n2. 玩家可以选择抽取一张新牌或者保留当前的牌。\n3. 游戏结束时，拥有点数最高的牌的玩家获胜。")

# 隐藏规则窗口
rules_frame.pack_forget()

def toggle_frame(frame, button):
    """
    展开或折叠Frame
    """
    if frame.winfo_viewable():
        frame.pack_forget()
        button.config(text="规则")
    else:
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        button.config(text="关闭")

# 运行窗口
output_window.mainloop()