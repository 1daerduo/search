# -*- coding: utf-8 -*-
import re
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import json
import sys
import datetime
from collections import OrderedDict
from tkinter import scrolledtext
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
        else:
            params[key.lower()] = value
        
print('所有参数：')
for key, value in params.items():
    print(f'{key}: {value}')


if 'H' in params or 'h' in params or 'help' in params:
    print()
    print('*********************************************')
    print('--: 以下为支持参数(包含"-"):                *')
    print('-h: 获取参数帮助                            *')
    print('-s: 默认排序                                *')
    print('示例: python streamfind-HB3.py -s           *')
    print('*********************************************')
    sys.exit()
# 创建Tkinter窗口
root = tk.Tk()
root.withdraw()

# 打开文件选择对话框
#file_path = filedialog.askopenfilename()
file_paths = filedialog.askopenfilenames(title='选择日志文件')


# 打开选择的文件
# 运行时间和出流时间的统计
stream_dict = {}
for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # 使用正则表达式匹配数字
    #pattern = r"camera_.*, SN:([A-Z0-9]{16}), open_duration:(\d+)ms.*stream_time:(\d+)ms"
    pattern = r"Baize_StrategyModEntry:.*] camera_(\d+), llRecordID:.*, record_time:(\d+) ms, record_valid:.*"
    matches = re.findall(pattern, text)
    
    pattern1 = r"camera_(\d+).*(T[A-Z0-9]{15})"
    matches1 = re.findall(pattern1, text)
    # 将所有匹配到的流时间求和
    for match in matches:
        if stream_dict.get(match[0]) == None:
            stream_dict[match[0]] = {}
            stream_dict[match[0]]['count'] = 0
            stream_dict[match[0]]['total_record'] = 0
            stream_dict[match[0]]['total_duration_stream'] = 0
        stream_dict[match[0]]['count'] += 1
        stream_dict[match[0]]['total_record'] += int(match[1])
        #stream_dict[match[0]]['total_duration_stream'] += int(match[2])
    for match in matches1:
        if stream_dict.get(match[0]) != None:
            stream_dict[match[0]]['SN'] = match[1]

print('stream_dict\r\n', stream_dict)
#for num in stream_dict:
#   print('cam:',num, '录像次数:', stream_dict[num]['count'], '总计运行时间(ms):',stream_dict[num]['total_record'])
    
# 修改顺序
print()
sorted_dict = stream_dict
if 's' in params:
    sorted_dict = dict(sorted(stream_dict.items()))
#elif 'k' in params:
#    sorted_dict = dict(sorted(stream_dict.items(), key=lambda x: x[0]))
for num in sorted_dict:
    print('cam:',num, 'SN:', stream_dict[num].get('SN', 'N/A'),'录像计数:', sorted_dict[num]['count'], '总计运行时间(ms):',sorted_dict[num]['total_record'])