import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db

# Store ID with Name
def load_students():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, student_name FROM students")
    students = cursor.fetchall()
    conn.close()
    return students

def save_subject(student_id, semester, subject_name, marks):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO subjects (student_id, semester, subject_name, marks) VALUES (?, ?, ?, ?)",
        (student_id, semester, subject_name, marks)
    )
    conn.commit()
    conn.close()

def add_subject_form():
    form = tk.Toplevel()
    form.title("Add Subject")

    # Load students from DB
    students = load_students()
    student_dict = {name: sid for sid, name in students}
    student_names = list(student_dict.keys())

    tk.Label(form, text="Select Student:").pack(pady=5)
    student_combo = ttk.Combobox(form, values=student_names)
    student_combo.pack(pady=5)

    tk.Label(form, text="Semester:").pack(pady=5)
    semester_combo = ttk.Combobox(form, values=[1, 2, 3, 4])
    semester_combo.pack(pady=5)

    tk.Label(form, text="Subject Name:").pack(pady=5)
    subject_name = tk.Entry(form)
    subject_name.pack(pady=5)

    tk.Label(form, text="Marks:").pack(pady=5)
    marks = tk.Entry(form)
    marks.pack(pady=5)

    def on_submit():
        selected_student = student_combo.get()
        if selected_student not in student_dict:
            messagebox.showerror("Error", "Please select a valid student.")
            return

        student_id = student_dict[selected_student]
        save_subject(student_id, semester_combo.get(), subject_name.get(), marks.get())
        messagebox.showinfo("Success", "Subject added successfully!")
        form.destroy()

    tk.Button(form, text="Submit", command=on_submit).pack(pady=10)
    tk.Button(form, text="Cancel", command=form.destroy).pack(pady=5)

    form.mainloop()
