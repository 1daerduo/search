import tkinter as tk
from tkinter import filedialog
import pandas as pd
import re
import json

# 创建窗口
root = tk.Tk()
root.withdraw()

# 选择日志文件
log_file_path = filedialog.askopenfilename(title='选择日志文件', filetypes=[('日志文件', '*.txt')])

# 选择规则文件
rules_file_path = filedialog.askopenfilename(title='选择规则文件', filetypes=[('Excel文件', '*.xlsx')])

try:
    # 读取规则文件
    df = pd.read_excel(rules_file_path)
except Exception as e:
    print(f"读取规则文件失败：{e}")
    exit()

# 创建输出字典
output_dict = {}

# 遍历每一行规则
for index, row in df.iterrows():
    pattern = row['规则']  # 获取规则
    result = row['结果']   # 获取结果

    # 创建一个列表，用于存储匹配结果
    matches = []

    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if re.search(pattern, line):
                    matches.append(f"Line {i}: {line.strip()}")  # 将匹配结果添加到列表中
    except Exception as e:
        print(f"读取日志文件失败：{e}")
        exit()

    # 如果有匹配结果，则输出匹配结果
    if matches:
        # 将匹配结果添加到输出字典中
        output_dict[pattern] = {
            '结果': result,
            '匹配项': matches
        }

# 将输出字典写入JSON文件
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(output_dict, f, ensure_ascii=False, indent=4)

# 创建输出窗口和Frame
output_window = tk.Toplevel()
output_window.title('输出结果')

output_frame = tk.Frame(output_window)
output_frame.pack(fill='both', expand=True)

# 创建文本框
output_text = tk.Text(output_frame, wrap='word', font=('Arial', 12))
output_text.pack(fill='both', expand=True)

# 读取JSON文件并将内容显示在文本框中
with open('output.json', 'r', encoding='utf-8') as f:
    output_text.insert('end', f.read())

output_text.config(state='disabled')  # 禁止编辑文本框

print("输出完成！")