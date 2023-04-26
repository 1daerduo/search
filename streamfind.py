import re
import tkinter as tk
from tkinter import filedialog

# 创建Tkinter窗口
root = tk.Tk()
root.withdraw()

# 打开文件选择对话框
file_path = filedialog.askopenfilename()

# 打开选择的文件
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 使用正则表达式匹配数字
pattern = r"camera_0, SN:T8210.*, open_duration:(\d+)ms"
matches = re.findall(pattern, text)

# 将所有匹配到的数字叠加起来
total_duration = 0
count = 0
for match in matches:
    print('count',count, 'match', match)
    count += 1
    total_duration += int(match)

print(total_duration)