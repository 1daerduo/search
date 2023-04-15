import tkinter as tk
from tkinter import filedialog
import pandas as pd
import re
import json
import sys
import datetime

def read_rules(rule_file):
    rules = []
    with open(rule_file, 'r') as f:
        for line in f:
            sub_rules = line.strip().split('\n')
            rules.append(sub_rules)
    return rules

def match_rule(rule, log):
    matched_sub_rules = []
    for sub_rule in rule:
        regex = re.compile(sub_rule)
        if regex.search(log):
            matched_sub_rules.append(sub_rule)
    if len(matched_sub_rules) == len(rule):
        return True, matched_sub_rules
    else:
        return False, []

df = None
def search_log(log_file, rules):
    global df
    output_dict = {}
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            for index, rule in enumerate(rules):
                is_matched, matched_sub_rules = match_rule(rule, line)
                if is_matched:
                    pattern = ''.join(rule)
                    if pattern not in output_dict:
                        output_dict[pattern] = {
                            '结果': '',
                            '匹配项': []
                        }
                    output_dict[pattern]['匹配项'].append(f"Line {index+1}: {line.strip()}")
                    if len(output_dict[pattern]['匹配项']) == len(rule):
                        result = df.loc[df['规则']==pattern, '结果'].values[0]
                        output_dict[pattern]['结果'] = f"{result}，匹配次数：{len(rule)}"
                        break

    return output_dict

# 创建窗口
root = tk.Tk()
root.withdraw()

# 选择日志文件
log_file_path = filedialog.askopenfilename(title='选择日志文件', filetypes=[('日志文件', '*.txt')])

# 选择规则文件
rules_file_path = filedialog.askopenfilename(title='选择规则文件', filetypes=[('Excel文件', '*.xlsx')])

try:
    # 读取规则文件
    df = pd.read_excel(rules_file_path)
except Exception as e:
    print(f"读取规则文件失败：{e}")
    exit()

# 将规则文件中的规则拆分成多个子规则
rules = []
for index, row in df.iterrows():
    sub_rules = row['规则'].strip().split('\n')
    rules.append(sub_rules)

# 打印拆分后的规则
for rule in rules:
    print(rule)
# 搜索日志文件并获取匹配结果
output_dict = search_log(log_file_path, rules)

# 判断是否有输入T字母
if 't' in [arg.lower() for arg in sys.argv]:
    # 获取当前日期和时间
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{now}_output.json"
else:
    filename = "output.json"

# 将输出字典写入JSON文件
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(output_dict, f, ensure_ascii=False, indent=4)

# 创建输出窗口和Frame
output_window = tk.Toplevel()
output_window.title('输出结果')

output_frame = tk.Frame(output_window)
output_frame.pack(fill='both', expand=True)

# 创建文本框
output_text = tk.Text(output_frame, wrap='word', font=('Arial', 12))
output_text.pack(fill='both', expand=True)

# 读取JSON文件并将内容显示在文本框中
with open(filename, 'r', encoding='utf-8') as f:
    output_text.insert('end', f.read())

output_text.config(state='disabled')  # 禁止编辑文本框

print("输出完成！")
