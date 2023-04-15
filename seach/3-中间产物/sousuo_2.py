import pandas as pd
import re

# 读取Excel文件
df = pd.read_excel('rules.xlsx')

# 遍历每一行规则
for index, row in df.iterrows():
    pattern = row['规则']  # 获取规则
    result = row['结果']   # 获取结果

    # 打开日志文件
    with open('log.txt', 'r') as f:
        # 逐行扫描日志文件
        for line in f:
            # 使用正则表达式匹配字符串
            if re.search(pattern, line):
                print(result)  # 输出匹配结果