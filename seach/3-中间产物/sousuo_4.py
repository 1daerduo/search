import tkinter as tk
from tkinter import filedialog
import pandas as pd
import re

# 创建窗口
root = tk.Tk()
root.withdraw()

# 选择日志文件
log_file_path = filedialog.askopenfilename(title='选择日志文件', filetypes=[('日志文件', '*.txt')])

# 选择规则文件
rules_file_path = filedialog.askopenfilename(title='选择规则文件', filetypes=[('Excel文件', '*.xlsx')])

# 读取规则文件
df = pd.read_excel(rules_file_path)

# 创建输出窗口
output_window = tk.Tk()
output_window.title('匹配结果')

# 创建输出框
output_text = tk.Text(output_window)
output_text.pack()

# 遍历每一行规则
for index, row in df.iterrows():
    pattern = row['规则']  # 获取规则
    result = row['结果']   # 获取结果

    # 打开日志文件
    with open(log_file_path, 'r', encoding='utf-8') as f:
        # 逐行扫描日志文件
        for i, line in enumerate(f, 1):
            # 使用正则表达式匹配字符串
            if re.search(pattern, line):
                output_text.insert(tk.END, f"Line {i}: {result}\n")  # 输出匹配结果和行号

# 运行窗口
output_window.mainloop()