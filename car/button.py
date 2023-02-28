import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# 创建一个ttk风格
style = ttk.Style()

# 为风格定义主题
style.theme_create("mytheme", parent="clam", settings={
    "TButton": {
        "configure": {"background": "#ff0000", "foreground": "#ffffff"},
        "map": {
            "background": [("active", "#ff3333"), ("pressed", "#ff0000")],
            "foreground": [("active", "#ffffff"), ("pressed", "#ffffff")]
        }
    }
})

# 设置当前使用的ttk主题
style.theme_use("mytheme")

# 创建一个ttk按钮
button = ttk.Button(root, text="Click me")
button.pack()

root.mainloop()