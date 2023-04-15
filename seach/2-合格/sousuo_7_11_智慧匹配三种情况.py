import tkinter as tk
from tkinter import filedialog
import pandas as pd
import re
import json
import sys
import datetime

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

# 创建规则列表
rules = list(df['规则'])

try:
    with open(log_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            for rule in rules:
                if re.search(rule, line):
                    # 匹配到规则后，将规则添加到输出字典中
                    if rule not in output_dict:
                        output_dict[rule] = {'匹配项': []}
                    output_dict[rule]['匹配项'].append(line.strip())
                    rules.remove(rule)  # 匹配到规则后，从列表中删除该规则
                    break  # 匹配到规则后，跳出内层循环

            if not rules:  # 如果规则列表为空，说明匹配成功
                break  # 跳出外层循环
except Exception as e:
    print(f"读取日志文件失败：{e}")
    exit()

# 遍历每一行规则
for index, row in df.iterrows():
    pattern = row['规则']  # 获取规则
    result = row['结果']   # 获取结果

    # 如果规则已经在输出字典中，说明已经匹配到了，跳过该规则
    #if pattern in output_dict:
    #    continue

    # 创建一个列表，用于存储匹配结果
    matches = []

    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            count = 0  # 记录匹配次数
            for i, line in enumerate(f, 1):
                if re.search(pattern, line):
                    count += 1  # 匹配次数加1
                    matches.append(f"Line {i}: {line.strip()}")  # 将匹配结果添加到列表中
    except Exception as e:
        print(f"读取日志文件失败：{e}")
        exit()

    # 如果有匹配结果，则将规则和匹配结果添加到输出字典中
    if matches:
        output_dict[pattern] = {
            '结果': f"{result}，匹配次数：{count}",  # 将匹配次数添加到结果中
            '匹配项': matches
        }

# 统计有结果的规则数量
matched_rules_count = len([rule for rule in output_dict if output_dict[rule]])

# 判断是否有输入T字母
if 't' in [arg.lower() for arg in sys.argv]:
    # 获取当前日期和时间
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{now}_output.json"
else:
    filename = "output.json"

# 将输出字典写入JSON文件
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(output_dict, f, ensure_ascii=False, indent=4)

# 判断是否所有规则都匹配成功
if len(output_dict) == len(df):
    print("已匹配所有规则，输出完成！")
elif matched_rules_count == 0:
    print("没有匹配到任何规则！")
else:
    print(f"已匹配{matched_rules_count}条规则，输出完成！")
    
# 遍历输出字典，输出匹配结果
for rule in output_dict:
    if output_dict[rule]:
        #print(f"规则：{rule}")
        print(f"结果：{output_dict[rule]['结果']}")
        #print(f"匹配项：{output_dict[rule]['匹配项']}")
            
    # 创建输出窗口和Frame
    output_window = tk.Toplevel()
    output_window.title('输出结果')

    output_frame = tk.Frame(output_window)
    output_frame.pack(fill='both', expand=True)

    # 创建文本框
    output_text = tk.Text(output_frame, wrap='word', font=('Arial', 12))
    output_text.pack(fill='both', expand=True)

    # 遍历输出字典，将内容显示在文本框中
    for rule in output_dict:
        if output_dict[rule]:
            output_text.insert('end', f"规则：{rule}\n")
            output_text.insert('end', f"结果：{output_dict[rule]['结果']}\n")
            output_text.insert('end', "匹配项：\n")
            for item in output_dict[rule]['匹配项']:
                output_text.insert('end', f"{item}\n")
            output_text.insert('end', "\n")

    output_text.config(state='disabled')  # 禁止编辑文本框
