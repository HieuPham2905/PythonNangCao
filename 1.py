import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime

# Hàm xử lý sự kiện khi nhấn nút "Click Me!"
def on_button_click():
    try:
        # Lấy văn bản từ Entry và năm sinh từ Entry khác
        name = entry.get()
        birth_year = int(year_entry.get())
        current_year = datetime.now().year

        # Kiểm tra nếu năm sinh không hợp lệ
        if birth_year > current_year or birth_year < 1900:
            button.config(text="Năm sinh không tồn tại")
        else:
            age = current_year - birth_year
            # Thay đổi văn bản của nút Button
            button.config(text=f"Hello {name}, you are {age} years old")
    except ValueError:
        button.config(text="Vui lòng nhập năm hợp lệ")

# Hàm thay đổi màu nền của cửa sổ dựa trên lựa chọn của Radio Button
def change_color():
    color = color_var.get()
    root.configure(bg=color)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Python GUI")
root.geometry("550x250")
root.resizable(False, False)

# Tạo Frame chính để chứa các widget
main_frame = ttk.LabelFrame(root, text='Main Frame')
main_frame.grid(column=0, row=0, padx=10, pady=10)

# Label và Entry để nhập tên
label = tk.Label(main_frame, text="Enter your name:")
label.grid(column=0, row=0, sticky='W', padx=10, pady=5)

entry = tk.Entry(main_frame, width=40)
entry.grid(column=1, row=0, padx=10, pady=5)

# Label và Entry để nhập năm sinh
year_label = tk.Label(main_frame, text="Enter your birth year:")
year_label.grid(column=0, row=1, sticky='W', padx=10, pady=5)

year_entry = tk.Entry(main_frame, width=12)
year_entry.grid(column=1, row=1, padx=10, pady=5)

# Nút bấm "Click Me!"
button = tk.Button(main_frame, text="Click Me!", command=on_button_click)
button.grid(column=1, row=2, padx=10, pady=5)

# Label cho các Radio Button
color_label = tk.Label(main_frame, text="Select a color:")
color_label.grid(column=0, row=5, sticky='W', padx=10, pady=5)

# Biến để lưu giá trị Radio Button
color_var = tk.StringVar()
color_var.set("white")  # Giá trị mặc định

# Tạo các Radio Button
radio_blue = tk.Radiobutton(main_frame, text="Blue", variable=color_var, value="blue", command=change_color)
radio_blue.grid(column=0, row=6, sticky='W', padx=10, pady=5)

radio_gold = tk.Radiobutton(main_frame, text="Gold", variable=color_var, value="gold", command=change_color)
radio_gold.grid(column=1, row=6, sticky='W', padx=10, pady=5)

radio_red = tk.Radiobutton(main_frame, text="Red", variable=color_var, value="red", command=change_color)
radio_red.grid(column=2, row=6, sticky='W', padx=10, pady=5)

# Hiển thị cửa sổ chính
root.mainloop()
