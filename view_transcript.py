import tkinter as tk
from tkinter import ttk
from database import connect_db

def load_roll_nos():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT roll_no FROM students")
    roll_nos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return roll_nos

def view_transcript_form():
    form = tk.Toplevel()
    form.title("View Transcript")

    tk.Label(form, text="Select Roll No:").pack(pady=5)
    roll_combo = ttk.Combobox(form, values=load_roll_nos())
    roll_combo.pack(pady=5)

    tree = ttk.Treeview(form, columns=("Name", "Semester", "Subject", "Marks"), show="headings")
    tree.heading("Name", text="Student Name")
    tree.heading("Semester", text="Semester")
    tree.heading("Subject", text="Subject Name")
    tree.heading("Marks", text="Marks")
    tree.pack(fill="both", expand=True)

    def on_search():
        roll_no = roll_combo.get()
        if roll_no:
            for item in tree.get_children():
                tree.delete(item)

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT student_name, semester, subject_name, marks
                FROM subjects
                INNER JOIN students ON subjects.student_id = students.id
                WHERE roll_no = ?
                ORDER BY semester
            """, (roll_no,))
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=row)
            conn.close()

    def generate_transcript():
        roll_no = roll_combo.get()
        if not roll_no:
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT semester, marks
            FROM subjects
            INNER JOIN students ON subjects.student_id = students.id
            WHERE roll_no = ?
        """, (roll_no,))
        data = cursor.fetchall()
        conn.close()

        # Organize marks by semester
        semester_marks = {}
        for semester, marks in data:
            semester_marks.setdefault(semester, []).append(marks)

        # GPA and CGPA Calculation
        gpa_by_semester = {}
        for sem, marks_list in semester_marks.items():
            avg_marks = sum(marks_list) / len(marks_list)
            gpa = round(avg_marks / 25, 2)  # Example: 100 marks = 4.0 GPA
            gpa_by_semester[sem] = gpa

        cgpa = round(sum(gpa_by_semester.values()) / len(gpa_by_semester), 2) if gpa_by_semester else 0.0

        # Open new window with results
        summary = tk.Toplevel()
        summary.title("Transcript Summary")

        tk.Label(summary, text=f"Transcript Summary for Roll No: {roll_no}", font=("Arial", 12, "bold")).pack(pady=10)

        for sem in sorted(gpa_by_semester.keys()):
            tk.Label(summary, text=f"Semester {sem}: GPA = {gpa_by_semester[sem]}").pack()

        tk.Label(summary, text=f"\nCGPA: {cgpa}", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Button(form, text="Search", command=on_search).pack(pady=10)
    tk.Button(form, text="Generate Transcript", command=generate_transcript).pack(pady=5)

    form.mainloop()
