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
EffectiveVideo = {}
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
            stream_dict[match[1]]['camera_' + match[0]]['出流耗时(ms)'] = 0           

        stream_dict[match[1]]['camera_' + match[0]]['统计次数'] += 1
        stream_dict[match[1]]['camera_' + match[0]]['总运行时间(ms)'] += int(match[2])
        stream_dict[match[1]]['camera_' + match[0]]['出流耗时(ms)'] += int(match[3])

    # 获取总录像次数
    pattern = r"zyy camera_(\d+), dev_type:(\d+), has_mdetect_even:.*, has_human:0x.*, record_file_state:.*, frame_num:.*, discard_record_flag:0x(\d+)"
    matches_videos = re.findall(pattern, text)    
    for match in matches_videos:
        if EffectiveVideo.get('camera_' + match[0]) == None:
            EffectiveVideo['camera_' + match[0]] = {}
            EffectiveVideo['camera_' + match[0]]['总录像'] = 0
            EffectiveVideo['camera_' + match[0]]['有效录像'] = 0
            EffectiveVideo['camera_' + match[0]]['设备类型'] = int(match[1])
            EffectiveVideo['camera_' + match[0]]['无效'] = {}
            
        EffectiveVideo['camera_' + match[0]]['总录像'] += 1
        #print('match[2]:', int(match[2]))
        if int(match[2]) == 0:
            EffectiveVideo['camera_' + match[0]]['有效录像'] += 1
        else:
            if (EffectiveVideo['camera_' + match[0]]['无效']).get('总记') == None:
                EffectiveVideo['camera_' + match[0]]['无效']['总记'] = 0
            EffectiveVideo['camera_' + match[0]]['无效']['总记'] += 1  
            
            if (EffectiveVideo['camera_' + match[0]]['无效']).get(match[2]) == None:
                EffectiveVideo['camera_' + match[0]]['无效'][match[2]] = 0
            EffectiveVideo['camera_' + match[0]]['无效'][match[2]] += 1

print('出流统计:\n', json.dumps(stream_dict, indent=4, ensure_ascii=False))
print()
print('录像统计:\n', json.dumps(EffectiveVideo, indent=4, ensure_ascii=False))
