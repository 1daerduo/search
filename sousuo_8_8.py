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
params = {}
for arg in sys.argv[1:]:
    if arg.startswith('-'):
        params[arg[1:].lower()] = True
    else:
        key, value = arg.split('=')
        params[key.lower()] = value
        
print('所有参数：')
for key, value in params.items():
    print(f'{key}: {value}')
    
# 2.如果参数中有“a”或者“A”，调用#4的程序时候，使用的规则结构是所有工作表的规则，
# 如果没有则提示使用者指定工作表，然后调用#4时使用指定的工作表的规则（即只匹配其中一个工作表）。
if 'a' in params or 'A' in params:
    all_tables = True
else:
    all_tables = False
    #table_name = input("请输入要读取的工作表名称或索引：")
    if 'table' not in params:
        print('请指定需要匹配的工作表')
        sys.exit()
    else:
        table_name = params['table']

# 3.打开规则文件，读取其内包括的所有工作表的名称，存储到一个规则结构中，
# 并且结构按照规则表来区分。
rules = OrderedDict()
with pd.ExcelFile(rules_file_path) as xls:
    for sheet_name in xls.sheet_names:
        rules[sheet_name] = pd.read_excel(xls, sheet_name).fillna('')

# 3.1然后创建一个全局json结构
output = {}

# 4.打开规则文件读取某一个工作表中的所有规则，存储到结构中；
for table, rule_df in rules.items():
    if not all_tables and table != table_name:
        continue
    output[table] = {}
    for _, rule in rule_df.iterrows():
        regex = re.compile(rule['规则'])
        count = 0
        match_lines = []
        with open(log_file_path, 'r', encoding='utf-8') as log_file:
            for line_num, line in enumerate(log_file):
                if regex.search(line):
                    count += 1
                    match_lines.append(f'{line_num} {line.strip()}')
        if count > 0:
            output[table][rule['规则']] = {
                '匹配项目': match_lines,
                '次数': count,
                '结果': rule['结果']
            }
        if len(output[table]) == len(rule_df):
            output[table]['判定'] = '成功'
        else:
            output[table]['判定'] = '失败'

# 5.匹配工作完成
# 5.1 输出json文本
if 't' in params or 'T' in params:
    json_file_name = f'output_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.json'
else:
    json_file_name = 'output.json'
with open(json_file_name, 'w', encoding='utf-8') as output_file:
    json.dump(output, output_file, ensure_ascii=False, indent=4)

# 6.如果输出的参数有“w”或者“W”，需要将这些json文本以方便查看的方式输出到windown窗口。
if 'w' in params or 'W' in params:
    with open(json_file_name, 'r', encoding='utf-8') as output_file:
        output_text = output_file.read()
    root = tk.Tk()
    root.title('匹配结果')
    text = tk.Text(root)
    text.pack()
    text.insert('end', output_text)
    root.mainloop()

# 7.对于#4.2.5的匹配结果应该输出到CMD窗口，让运行者第一时间直到整个匹配的结果。
for table, result in output.items():
    print(f'工作表：{table}')
    for rule, info in result.items():
        if rule != '判定':
            print(f'规则：{rule}，次数：{info["次数"]}，结果：{info["结果"]}')
            print('匹配项目：')
            for line in info['匹配项目']:
                print(line)
            print()
    print(f'判定：{result["判定"]}')
    print()