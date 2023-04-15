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

# 选择规则文件，规则文件的中每个工作边又两列分别为：”规则“和”结果“
rules_file_path = filedialog.askopenfilename(title='选择规则文件', filetypes=[('Excel文件', '*.xlsx')])

# 1.获取参数，存储到一个参数结构中。
args = sys.argv[1:]

# 2.打开规则文件，读取其内包括的所有工作表的名称，存储到一个规则结构中，并且结构按照规则表来区分。
# 2.1然后创建一个全局json结构
rules = OrderedDict()
with pd.ExcelFile(rules_file_path) as xls:
    for sheet_name in xls.sheet_names:
        rules[sheet_name] = OrderedDict()

# 3.打开规则文件读取某一个工作表中的所有规则，存储到结构中；
# 3.1.json结构中添加以工作表为名的对象。{"工作名":{}}
# 3.1.打开日志文件对，读取一条规则结构的”规则“，用正则表达式在日志文件中查找规则。
# 3.2.每匹配到一次，就计数器count+=1，记录匹配到的行号，将行号与匹配行组合起来成新的文本，如果
# count>0, 在接”工作表“对象中添加以”规则“为名的结构{"工作名":{”规则“:{}}}；
# 1.在”规则“结构中添加键值对，内容是：
# "匹配项目":["行号 匹配行内容"，"行号 匹配行内容"],则json结构为{"工作名":{"规则":{}}；
# 2.在”规则“结构中添加键值对，内容是：
# "次数":"count",则json结构为{"工作名":{"规则":{"匹配项目":["行号 匹配行内容","行号 匹配行内容"],"次数":"count"}}}；
# 3.在”规则“结构中添加键值对，内容是：
# "结果":"规则列的结果",则json结构为{"工作名":{"规则":{"匹配项目":["行号 匹配行内容","行号 匹配行内容"],"次数":"count","结果":"规则列的结果"}}}；
# 4.循环匹配每一行规则。123
# 5.如果所有的规则都能在日志文件中找到，则在“工作名”结构中添加键值对，内容是：
# "判定":"成功"，则json结构为{"工作名":{"规则":{"匹配项目":["行号 匹配行内容","行号 匹配行内容"],"次数":"count","结果":"规则列的结果"},"判定":"成功"}}
# 如果不是所有都匹配成功，则在“工作名”结构中添加键值对，内容是：
# "判定":"失败"，则json结构为{"工作名":{"规则":{"匹配项目":["行号 匹配行内容","行号 匹配行内容"],"次数":"count","结果":"规则列的结果"},"判定":"失败"}}
for sheet_name in rules:
    sheet = pd.read_excel(rules_file_path, sheet_name=sheet_name)
    for index, row in sheet.iterrows():
        rule = row['规则']
        result = row['结果']
        regex = re.compile(rule)
        count = 0
        matches = []
        with open(log_file_path, 'r', encoding='utf-8') as log_file:
            for line_num, line in enumerate(log_file):
                if regex.search(line):
                    count += 1
                    matches.append(f"{line_num} {line.strip()}")
        if count > 0:
            rules[sheet_name][rule] = {
                "匹配项目": matches,
                "次数": count,
                "结果": result
            }
    if len(rules[sheet_name]) == len(sheet):
        rules[sheet_name]["判定"] = "成功"
    else:
        rules[sheet_name]["判定"] = "失败"

# 4.如果参数中有“a”或者“A”，调用#3的程序使用的规则结构是所有工作表的规则，如果没有则提示使用者指定工作表，然后调用#3时使用指定工作表的规则。
if 'a' in args or 'A' in args:
    pass
else:
    sheet_name = input("请输入要匹配的工作表名称：")
    if sheet_name in rules:
        sheet_rules = rules[sheet_name]
    else:
        print("工作表名称不存在")
        sys.exit()

# 5.匹配工作完成
# 5.1 输出json文本
# 5.1.1 如果参数带着大小写“t”or“T”,则将json文件名 需要根据当前日期和时间命名
# 5.1.2 如果参数不带带着大小写“t”or“T”,则将json文件名 命名为“output.json”
# 5.1.2 输出json结构到json文件。
output_file_name = "output.json"
if 't' in args or 'T' in args:
    now = datetime.datetime.now()
    output_file_name = f"output_{now.strftime('%Y-%m-%d_%H-%M-%S')}.json"

with open(output_file_name, 'w', encoding='utf-8') as output_file:
    json.dump(rules, output_file, ensure_ascii=False, indent=4)