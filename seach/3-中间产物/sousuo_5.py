import re

def find_matches(pattern, text):
    lines = text.split("\n")
    matches = []
    count = 0
    for i, line in enumerate(lines):
        for match in re.finditer(pattern, line):
            count += 1
            start = match.start()
            end = match.end()
            matches.append((i, start, end))
    if count == 0:
        print("No matches found.")
    else:
        print(f"{count} matches found.")
        for i, match in enumerate(matches):
            line_num, start, end = match
            link = f"<a href='#{i+1}'>Match {i+1}</a>"
            lines[line_num] = f"{lines[line_num][:start]}{link}{lines[line_num][end:]}"
        return "\n".join(lines)

# 读取日志文件
with open("log.txt", "r") as f:
    text = f.read()

# 搜索文本
pattern = r"query_other_record_related_table_data"
result = find_matches(pattern, text)

# 生成 HTML 页面
html = f"""
<html>
<head>
    <title>Log Search Results</title>
</head>
<body>
    <h1>Log Search Results</h1>
    <p>Search pattern: {pattern}</p>
    <pre>{result}</pre>
</body>
</html>
"""

# 将 HTML 页面保存到文件
with open("result.html", "w") as f:
    f.write(html)