import tkinter as tk
from tkinter import ttk
import psycopg2
from psycopg2 import sql
from tkinter import messagebox

def connect_db():
    try:
        conn = psycopg2.connect(
            database="postgres",       
            user="postgres",          
            password="phattan112",     
            host="localhost",
            port="5432"
        )
        
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INTEGER,
                gender VARCHAR(10),
                major VARCHAR(100)
            )
        """)
        conn.commit()
        cursor.close()
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

def load_data():
    for row in tree.get_children():
        tree.delete(row)
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert('', tk.END, values=row)
            cursor.close()
        except Exception as e:
            print("Error loading data:", e)
        finally:
            conn.close()

def add_student():
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    gender = entry_gender.get().strip()
    major = entry_major.get().strip()
    
    if not name or not age:
        print("Name and Age are required fields.")
        return

    try:
        age_int = int(age)
    except ValueError:
        print("Age must be an integer.")
        return

    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (name, age, gender, major) 
                VALUES (%s, %s, %s, %s)
            """, (name, age_int, gender, major))
            conn.commit()
            print("Student added successfully.")
            cursor.close()

            entry_name.delete(0, tk.END)
            entry_age.delete(0, tk.END)
            entry_gender.delete(0, tk.END)
            entry_major.delete(0, tk.END)
            load_data()
        except Exception as e:
            print("Error adding student:", e)
        finally:
            conn.close()

def delete_student():
    selected = tree.selection()
    if selected:
        student_id = tree.item(selected[0])['values'][0]
        confirm = tk.messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sinh viên này?")
        if not confirm:
            return
        
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
                conn.commit()
                print("Student deleted successfully.")
                cursor.close()
                load_data()
            except Exception as e:
                print("Error deleting student:", e)
            finally:
                conn.close()
    else:
        print("No student selected for deletion.")

root = tk.Tk()
root.title("Quản Lý Thông Tin Sinh Viên")
root.geometry("600x400")  
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

tk.Label(top_frame, text="Tên:", width=10, anchor='w').grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(top_frame, width=25)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(top_frame, text="Tuổi:", width=10, anchor='w').grid(row=0, column=2, padx=5, pady=5)
entry_age = tk.Entry(top_frame, width=25)
entry_age.grid(row=0, column=3, padx=5, pady=5)

tk.Label(top_frame, text="Giới tính:", width=10, anchor='w').grid(row=1, column=0, padx=5, pady=5)
entry_gender = tk.Entry(top_frame, width=25)
entry_gender.grid(row=1, column=1, padx=5, pady=5)

tk.Label(top_frame, text="Ngành học:", width=10, anchor='w').grid(row=1, column=2, padx=5, pady=5)
entry_major = tk.Entry(top_frame, width=25)
entry_major.grid(row=1, column=3, padx=5, pady=5)

middle_frame = tk.Frame(root)
middle_frame.pack(pady=10)

btn_add = tk.Button(middle_frame, text="Thêm sinh viên", command=add_student, width=15)
btn_add.grid(row=0, column=0, padx=10)

btn_delete = tk.Button(middle_frame, text="Xóa sinh viên", command=delete_student, width=15)
btn_delete.grid(row=0, column=1, padx=10)

btn_reload = tk.Button(middle_frame, text="Tải lại danh sách", command=load_data, width=15)
btn_reload.grid(row=0, column=2, padx=10)

bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10, fill=tk.BOTH, expand=True)

columns = ("id", "name", "age", "gender", "major")
tree = ttk.Treeview(bottom_frame, columns=columns, show="headings")
tree.heading("id", text="ID")
tree.heading("name", text="Tên")
tree.heading("age", text="Tuổi")
tree.heading("gender", text="Giới tính")
tree.heading("major", text="Ngành học")

tree.column("id", width=50, anchor='center')
tree.column("name", width=150, anchor='center')
tree.column("age", width=50, anchor='center')
tree.column("gender", width=100, anchor='center')
tree.column("major", width=150, anchor='center')

scrollbar = ttk.Scrollbar(bottom_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(fill=tk.BOTH, expand=True)

load_data()

root.mainloop()
