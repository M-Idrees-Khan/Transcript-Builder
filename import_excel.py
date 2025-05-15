import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from database import connect_db

def import_excel_data():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls")])
    if file_path:
        df = pd.read_excel(file_path)
        conn = connect_db()
        cursor = conn.cursor()

        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO students (student_name, roll_no)
                VALUES (?, ?)
            """, (row['Student Name'], row['Roll No']))
            cursor.execute("""
                INSERT INTO subjects (student_id, semester, subject_name, marks)
                VALUES ((SELECT id FROM students WHERE roll_no = ?), ?, ?, ?)
            """, (row['Roll No'], row['Semester'], row['Subject Name'], row['Marks']))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Data imported successfully!")

def import_from_excel_form():
    form = tk.Toplevel()
    form.title("Import From Excel")

    tk.Button(form, text="Choose Excel File", command=import_excel_data).pack(pady=10)
    tk.Button(form, text="Cancel", command=form.destroy).pack(pady=10)

    form.mainloop()
