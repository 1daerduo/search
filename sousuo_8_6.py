import tkinter as tk
from tkinter import filedialog
import pandas as pd
import re
import json
import sys
import datetime
from collections import OrderedDict

# 创建窗口
root = tk.Tk()
root.withdraw()

# 选择日志文件
log_file_path = filedialog.askopenfilename(title='选择日志文件', filetypes=[('日志文件', '*.txt'),('日志文件', '*.log')])

# 选择规则文件
rules_file_path = filedialog.askopenfilename(title='选择规则文件', filetypes=[('Excel文件', '*.xlsx')])

# 获取要读取的工作表名称或索引
if 'a' in [arg.lower() for arg in sys.argv]:
    try:
        # 读取规则文件的所有工作表
        df_dict = pd.read_excel(rules_file_path, sheet_name=None)
        df_list = list(df_dict.values())
        df = pd.concat(df_list)
    except Exception as e:
        print(f"读取规则文件失败：{e}")
        exit()
else:
    if 'f' in [arg.lower() for arg in sys.argv]:
        sheet_name = input("请输入要读取的工作表名称或索引：")
    else:
        sheet_name = None

    try:
        # 读取规则文件指定的工作表
        df = pd.read_excel(rules_file_path, sheet_name=sheet_name)
    except Exception as e:
        print(f"读取规则文件失败：{e}")
        exit() 

# 创建输出字典
output_dict = OrderedDict()

# 创建规则列表
rules = list(df['规则'])

try:
    with open(log_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            for rule in rules:
                if re.search(rule, line):
                    # 匹配到规则后，将规则添加到输出字典中
                    if rule not in output_dict:
                        output_dict[rule] = {'匹配项': [], '结果': '', '工作表': str(df.loc[df['规则']==rule].index[0])}
                    output_dict[rule]['匹配项'].append(line.strip())
                    output_dict[rule]['结果'] = df.loc[df['规则']==rule, '结果'].values[0]  # 添加结果项
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
    if pattern in output_dict:
        continue

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
        output_dict[pattern] = {'匹配项': matches, '结果': result, '工作表': str(index)}

# 按照工作表名称或索引对输出字典进行分类
output_dict_by_sheet = OrderedDict()
for pattern, value in output_dict.items():
    sheet = value['工作表']
    if sheet not in output_dict_by_sheet:
        output_dict_by_sheet[sheet] = OrderedDict()
    output_dict_by_sheet[sheet][str(pattern)] = {'匹配项': value['匹配项'], '结果': value['结果']}

# 将输出字典转换为JSON格式并输出到文件中
output_json = json.dumps(output_dict_by_sheet, ensure_ascii=False, indent=4)
output_file_name = f"output_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"
with open(output_file_name, 'w', encoding='utf-8') as f:
    f.write(output_json)

print(f"输出文件已保存为 {output_file_name}")