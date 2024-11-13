import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def on_submit():
    name = name_entry.get()
    email = email_entry.get()

    if not name or not email:
        messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin.")
    else:
        messagebox.showinfo("Thông báo", f"Đăng ký thành công!\n"
                                         f"Họ và Tên: {name}\n"
                                         f"Email: {email}")
     
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        chat_box.delete(1.0, tk.END)


def calculate(operation):
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())

        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            if num2 == 0:
                result = "Lỗi: Chia cho 0"
            else:
                result = num1 / num2
        
        result_label.config(text=f"Kết quả: {result}")
    except ValueError:
        result_label.config(text="Lỗi: Vui lòng nhập số hợp lệ")


root = tk.Tk()
root.title("Thông tin người dùng và Máy tính ")
root.geometry("400x500")


notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")


tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Thông tin cá nhân")


frame1 = ttk.Frame(tab1, padding="10")
frame1.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))


name_label = ttk.Label(frame1, text="Họ và Tên:")
name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

name_entry = ttk.Entry(frame1, width=30)
name_entry.grid(row=0, column=1, padx=5, pady=5)

email_label = ttk.Label(frame1, text="Email:")
email_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

email_entry = ttk.Entry(frame1, width=30)
email_entry.grid(row=1, column=1, padx=5, pady=5)

chat_label = ttk.Label(frame1, text="Khung chat:")
chat_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

chat_box = tk.Text(frame1, width=30, height=5)
chat_box.grid(row=2, column=1, padx=5, pady=5)

submit_button = ttk.Button(frame1, text="Submit", command=on_submit)
submit_button.grid(row=3, column=0, columnspan=2, pady=10)


frame1.columnconfigure(0, weight=1)
frame1.columnconfigure(1, weight=2)


tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Tính toán")

frame2 = ttk.Frame(tab2, padding="10")
frame2.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))


label_num1 = ttk.Label(frame2, text="Số thứ nhất:")
label_num1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

entry_num1 = ttk.Entry(frame2, width=20)
entry_num1.grid(row=0, column=1, padx=5, pady=5)


label_num2 = ttk.Label(frame2, text="Số thứ hai:")
label_num2.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

entry_num2 = ttk.Entry(frame2, width=20)
entry_num2.grid(row=1, column=1, padx=5, pady=5)


calc_button_add = ttk.Button(frame2, text="+", command=lambda: calculate("+"))
calc_button_add.grid(row=2, column=0, padx=5, pady=5)

calc_button_sub = ttk.Button(frame2, text="-", command=lambda: calculate("-"))
calc_button_sub.grid(row=2, column=1, padx=5, pady=5)

calc_button_mul = ttk.Button(frame2, text="*", command=lambda: calculate("*"))
calc_button_mul.grid(row=2, column=2, padx=5, pady=5)

calc_button_div = ttk.Button(frame2, text="/", command=lambda: calculate("/"))
calc_button_div.grid(row=2, column=3, padx=5, pady=5)


result_label = ttk.Label(frame2, text="Kết quả: ")
result_label.grid(row=3, column=0, columnspan=4, pady=10)


root.mainloop()