import tkinter as tk

# 创建一个 tkinter 窗口
window = tk.Tk()

# 设置窗口大小
window.geometry("400x400")

# 创建一个 Frame，用于包含规则输入框
rule_frame = tk.Frame(window)
rule_frame.pack(side="top")

# 创建一个规则输入框
rule_entry = tk.Entry(rule_frame, width=30)
rule_entry.pack(side="left")

# 创建一个 "添加" 按钮，用于添加规则
def add_rule():
    # 创建一个 Frame，用于包含规则和删除按钮
    frame = tk.Frame(rule_frame)
    frame.pack(side="top", padx=5, pady=5)

    # 创建一个标签，用于显示规则内容
    label = tk.Label(frame, text=rule_entry.get())
    label.pack(side="left")

    # 创建一个 "删除" 按钮，用于删除该规则
    def delete_rule():
        frame.destroy()

    delete_button = tk.Button(frame, text="删除", command=delete_rule)
    delete_button.pack(side="right")

# 创建一个 "添加" 按钮
add_button = tk.Button(rule_frame, text="添加", command=add_rule)
add_button.pack(side="left")

# 创建一个 "展开/收起" 按钮
expand_button_text = tk.StringVar()
expand_button_text.set("展开")
def toggle_expand():
    if expand_button_text.get() == "展开":
        # 遍历所有子 Frame，将它们的显示设置为 True
        for child in rule_frame.winfo_children():
            child.pack_configure(fill="both", expand=True)
        expand_button_text.set("收起")
    else:
        # 遍历所有子 Frame，将它们的显示设置为 False，除了第一个子 Frame（即规则输入框）
        for child in rule_frame.winfo_children()[1:]:
            child.pack_forget()
        expand_button_text.set("展开")

expand_button = tk.Button(rule_frame, textvariable=expand_button_text, command=toggle_expand)
expand_button.pack(side="right")

# 运行窗口
window.mainloop()
