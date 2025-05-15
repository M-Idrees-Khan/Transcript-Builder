import tkinter as tk
from tkinter import messagebox
from database import connect_db

def save_student(student_name, roll_no):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (student_name, roll_no) VALUES (?, ?)", (student_name, roll_no))
    conn.commit()
    conn.close()

def add_student_form():
    form = tk.Toplevel()
    form.title("Add Student")

    tk.Label(form, text="Student Name:").pack(pady=5)
    student_name = tk.Entry(form)
    student_name.pack(pady=5)

    tk.Label(form, text="Roll No:").pack(pady=5)
    roll_no = tk.Entry(form)
    roll_no.pack(pady=5)

    def on_save():
        save_student(student_name.get(), roll_no.get())
        messagebox.showinfo("Success", "Student added successfully!")
        form.destroy()

    tk.Button(form, text="Save", command=on_save).pack(pady=10)
    tk.Button(form, text="Cancel", command=form.destroy).pack(pady=10)

    form.mainloop()
