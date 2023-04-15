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
output_width = int(screen_width * 0.95)  # 输出窗口宽度为屏幕宽度的80%
output_height = int(screen_height * 0.9)  # 输出窗口高度为屏幕高度的80%
output_x = int((screen_width - output_width) / 2)  # 输出窗口的x坐标为屏幕中心
output_y = int((screen_height - output_height) / 2)  # 输出窗口的y坐标为屏幕中心
output_window.geometry(f"{output_width}x{output_height}+{output_x}+{output_y}")

# 创建输出框
output_frame = tk.Frame(output_window)
output_frame.pack(fill=tk.BOTH, expand=True)

# 设置Grid布局的行和列
output_frame.rowconfigure(0, weight=1)
output_frame.columnconfigure(0, weight=1)

# 存储每个规则对应的Frame
rule_frames = {}

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
        text.grid_forget()

        # 将Frame存储到字典中
        if pattern in rule_frames:
            rule_frames[pattern].append(rule_frame)
        else:
            rule_frames[pattern] = [rule_frame]

# 设置输出框的大小和其他属性
output_frame.config(width=output_width, height=output_height)

def toggle_frame(frame, text):
    """
    展开或折叠Frame
    """
    # 获取当前规则对应的所有Frame
    pattern = get_pattern(frame)
    frames = rule_frames[pattern]

    if frame.winfo_viewable():
        # 折叠所有同类Frame
        for f in frames:
            f.grid_remove()
        text.set("展开")
    else:
        # 展开所有同类Frame
        for f in frames:
            f.grid()
        text.set("折叠")

def get_pattern(frame):
    """
    获取Frame对应的规则
    """
    for pattern, frames in rule_frames.items():
        if frame in frames:
            return pattern

# 运行窗口
output_window.mainloop()