# -*- coding: utf-8 -*-
import re
import tkinter as tk
from tkinter import filedialog

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

for num in stream_dict:
    print('cam:',num, '录像次数:', stream_dict[num]['count'], '总计运行时间(ms):',stream_dict[num]['total_record'])
    