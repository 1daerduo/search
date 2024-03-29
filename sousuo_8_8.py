#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog
import pandas as pd
import re
import json
import sys
import datetime
from collections import OrderedDict
from tkinter import scrolledtext
import os

# 创建窗口
root = tk.Tk()
root.withdraw()

current_dir = os.getcwd()
#print("Current directory:", current_dir)
output_dir = current_dir + '\output'
#print("output_dir:", output_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    #print(f"Directory '{output_dir}' created successfully!")
#else:
    #print(f"Directory '{output_dir}' already exists!")
    
# 1.获取参数，存储到一个参数结构中。
params = {}
table_get = []
for arg in sys.argv[1:]:
    if arg.startswith('-'):
        params[arg[1:].lower()] = True
    else:
        key, value = arg.split('=')
        #params[key.lower()] = value
        if key == 'table':
            table_get.append(value)
            params[key.lower()] = table_get
        elif key == 'name':
            params[key.lower()] = value
        
print('所有参数：')
for key, value in params.items():
    print(f'{key}: {value}')
    
if 'H' in params or 'h' in params or 'help' in params:
    print()
    print('*********************************************')
    print('--: 以下为支持参数(包含"-"):                *')
    print('-h: 获取参数帮助                            *')
    print('-t: 根据当前时间生成json文件                *')
    print('-w: windown窗口显示                         *')
    #print('-p: CMD窗口打印匹配                         *')
    print('-a: 选择所有的工作表                        *')
    print('-l: 选择抓取抓取匹配细节                    *')
    print('-from_reg:类似notepad的搜索列表，更好看     *')
    print('table=Sheet2: 选择Sheet2工作表(可多个表组合)*')
    print('name=T8210C: 添加自定义的文字作为json文件名 *')
    print('示例: python sousuo_8.8.py table=bind -t -w *')
    print('*********************************************')
    sys.exit()
    
# 2.如果参数中有“a”或者“A”，调用#4的程序时候，使用的规则结构是所有工作表的规则，
# 如果没有则提示使用者指定工作表，然后调用#4时使用指定的工作表的规则（即只匹配其中一个工作表）。
if 'a' in params or 'A' in params:
    all_tables = True
else:
    all_tables = False
    #table_name = input("请输入要读取的工作表名称或索引：")
    if 'table' not in params:
        print('请指定需要匹配的工作表 例如，test.py table=Sheet2')
        sys.exit()
    else:
        table_name = params['table']
        
# 选择日志文件
log_file_paths = filedialog.askopenfilenames(title='选择日志文件', filetypes=[('日志文件', '*.txt'),('日志文件', '*.log')])

# 选择规则文件，规则文件的中每个工作边又两列分别为：”规则“和”结果“
rules_file_path = filedialog.askopenfilename(title='选择规则文件', filetypes=[('Excel文件', '*.xlsx')])

# 3.打开规则文件，读取其内包括的所有工作表的名称，存储到一个规则结构中，
# 并且结构按照规则表来区分。
rules = OrderedDict()
with pd.ExcelFile(rules_file_path) as xls:
    for sheet_name in xls.sheet_names:
        rules[sheet_name] = pd.read_excel(xls, sheet_name).fillna('')

# 3.1然后创建一个全局json结构
output = {}

# from_reg 输出的json报表更好看，按照规则作为键，文件名作为子项
if 'from_reg' in params:     
    # 4.打开规则文件读取某一个工作表中的所有规则，存储到结构中；
        for table, rule_df in rules.items():
            if not all_tables and table not in table_name: #and table != table_name:
                continue
            output[table] = {}
            for _, rule in rule_df.iterrows():
                regex = re.compile(rule['规则'])
                count = 0
                regex_count = 0
                match_lines = []
                output[table][rule['规则']] = {}
                
                for log_file_path in log_file_paths:
                    output[table][rule['规则']][log_file_path] = {}
                    count = 0
                    match_lines = []
                    #print("log_file_path:", log_file_path)
                    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as log_file:
                        for line_num, line in enumerate(log_file):
                            if regex.search(line):
                                count += 1
                                match_lines.append(f'line-{line_num+1}  {line.strip()}')
                    if count > 0:
                        if 'l' in params or 'L' in params:
                            output[table][rule['规则']][log_file_path] = {
                                '结果': rule['结果'],                                       
                                '次数': count,
                                '匹配项目': match_lines
                            }
                        else:
                            output[table][rule['规则']][log_file_path] = {
                                '结果': rule['结果'],                                       
                                '次数': count,
                        }
                    regex_count +=  count   
                    output[table][rule['规则']][log_file_path + ' (匹配' + str(count) + '次) '] = output[table][rule['规则']][log_file_path]
                    output[table][rule['规则']].pop(log_file_path)
                
                if regex_count > 0:
                    output[table][rule['规则']]['所有文件查到次'] = regex_count
                else:
                    output[table][rule['规则']]['所有文件查到次'] = 0
                    
                output[table][rule['规则'] + ' (总计'+ str(regex_count) + '次) '] = output[table][rule['规则']]
                output[table].pop(rule['规则'])
                
else:
    for log_file_path in log_file_paths:    
    # 4.打开规则文件读取某一个工作表中的所有规则，存储到结构中；
        output[log_file_path] = {}
        for table, rule_df in rules.items():
            if not all_tables and table not in table_name: #and table != table_name:
                continue
            output[log_file_path][table] = {}
            for _, rule in rule_df.iterrows():
                regex = re.compile(rule['规则'])
                count = 0
                match_lines = []
                
                with open(log_file_path, 'r', encoding='utf-8') as log_file:
                    for line_num, line in enumerate(log_file):
                        if regex.search(line):
                            count += 1
                            match_lines.append(f'line-{line_num+1}  {line.strip()}')
                if count > 0:
                    if 'l' in params or 'L' in params:
                        output[log_file_path][table][rule['规则']] = {
                            '结果': rule['结果'],                                       
                            '次数': count,
                            '匹配项目': match_lines
                        }
                    else:
                        output[log_file_path][table][rule['规则']] = {
                            '结果': rule['结果'],                                       
                            '次数': count,
                        }                    
            if len(output[log_file_path][table]) == len(rule_df):
                output[log_file_path][table]['判定'] = '成功'
            else:
                output[log_file_path][table]['判定'] = '失败'
                failed_rules = set(rule_df['规则']) - set(output[log_file_path][table].keys())
                if not list(failed_rules):
                    print('没有未匹配的规则，可能规则表重复')
                    output[log_file_path][table]['判定'] = '成功'
                    output[log_file_path][table]['失败规则'] = '有规则表重复...请检查规则列'
                else:
                    output[log_file_path][table]['失败规则'] = list(failed_rules)



# 5.匹配工作完成
# 5.1 输出json文本
if 't' in params or 'T' in params or 'name' in params:
    json_file_name = 'output'
    if 'name' in params:
        json_file_name += f'_{params.get("name", "")}'
    if 't' in params or 'T' in params:
        json_file_name += f'_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}'
    json_file_name += '.json'
else:
    json_file_name = 'output.json'
with open(f'{output_dir}\{json_file_name}', 'w', encoding='utf-8') as output_file:
    json.dump(output, output_file, ensure_ascii=False, indent=4)

# 6.如果输出的参数有“w”或者“W”，需要将这些json文本以方便查看的方式输出到windown窗口。
if 'w' in params or 'W' in params:
    with open(json_file_name, 'r', encoding='utf-8') as output_file:
        output_data = json.load(output_file)
    output_text = json.dumps(output_data, indent=4, ensure_ascii=False)
    root = tk.Tk()
    root.title('匹配结果')
    text = scrolledtext.ScrolledText(root, wrap=tk.WORD)
    text.pack(expand=True, fill='both')
    text.tag_config('fail', foreground='red')
    text.insert('end', output_text)
    start = '1.0'
    while True:
        start = text.search('判定', start, stopindex='end')
        if not start:
            break
        end = f'{start}+{len(" 判定 :  失败")}c'
        text.tag_add('fail', start, end)
        start = end
    text.config(state='disabled')  # 禁止编辑
    root.mainloop()

# 7.对于#4.2.5的匹配结果应该输出到CMD窗口，让运行者第一时间直到整个匹配的结果。
# if 'p' in params or 'P' in params:
    # for table, result in output.items():
        # print(f'工作表：{table}')
        # for rule, info in result.items():
            # if rule != '判定' and rule != '失败规则':
                # #print(f'规则：{rule}，次数：{info["次数"]}，结果：{info["结果"]}')
                # #print('匹配项目：')
                # #for line in info['匹配项目']:
                # #    print(line)
                # print()
        # print(f'判定：{result["判定"]}')
        # print(f'失败规则：{result["失败规则"]}')
        # print()