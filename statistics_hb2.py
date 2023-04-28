#!usr/bin/env pyython3
# -*- coding: utf-8 -*-
import re
import tkinter as tk
from tkinter import filedialog
import json

# 创建Tkinter窗口
root = tk.Tk()
root.withdraw()

# 打开文件选择对话框
#file_path = filedialog.askopenfilename()
file_paths = filedialog.askopenfilenames(title='选择日志文件')

# 抓取SN号，基站SN号，pir触发次数，总pir录像，有效录像个数，录像文件名，录像错误码搜集，
# 打开选择的文件
stream_dict = {}
for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 使用正则表达式匹配数字
    pattern = r"camera_(\d+), SN:([A-Z0-9]{16}), open_duration:(\d+)ms.*stream_time:(\d+)ms"
    matches_stream = re.findall(pattern, text)

    # 将所有匹配到的流时间求和
    for match in matches_stream:
        if stream_dict.get(match[1]) == None:     
            stream_dict[match[1]] = {}
        if stream_dict[match[1]].get('camera_' + match[0]) == None:
            stream_dict[match[1]]['camera_' + match[0]] = {}
            stream_dict[match[1]]['camera_' + match[0]]['统计次数'] = 0
            stream_dict[match[1]]['camera_' + match[0]]['总运行时间(ms)'] = 0
            stream_dict[match[1]]['camera_' + match[0]]['总出流时间(ms)'] = 0           

        stream_dict[match[1]]['camera_' + match[0]]['统计次数'] += 1
        stream_dict[match[1]]['camera_' + match[0]]['总运行时间(ms)'] += int(match[2])
        stream_dict[match[1]]['camera_' + match[0]]['总出流时间(ms)'] += int(match[3])
    # 获取总录像次数
    pattern = r"zyy camera_.*, dev_type:.*, has_mdetect_even:.*, has_human:0x.*, record_file_state:.*, frame_num:.*, discard_record_flag:0x.*"
    matches_stream = re.findall(pattern, text)    

#for num in stream_dict:
#    print('SN:',num, '记录次数:', stream_dict[num]['count'], '总计运行时间(ms):',stream_dict[num]['total_duration'],'总计出流时间(ms):', stream_dict[num]['total_duration_stream'])

#print('stream_dict', stream_dict)

print(json.dumps(stream_dict, indent=4, ensure_ascii=False))
