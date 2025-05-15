# Import and initialize the database (creates tables if they don't exist)
from database import init_db  # Create tables if not exist
init_db()  # Execute the function to initialize the database

# Import Tkinter for GUI
import tkinter as tk
from tkinter import messagebox

# Import forms from different modules
from student_form import add_student_form        # Form to add a new student
from subject_form import add_subject_form        # Form to add a new subject and marks
from import_excel import import_from_excel_form  # Form to import data from Excel
from view_transcript import view_transcript_form # Form to view the transcript

# Functions to open each form when buttons are clicked
def open_add_student_form():
    add_student_form()

def open_add_subject_form():
    add_subject_form()

def open_import_excel_form():
    import_from_excel_form()

def open_view_transcript_form():
    view_transcript_form()

# Create the main application window
root = tk.Tk()
root.title("Transcript Builder")

# Add buttons to the main window for each feature
tk.Button(root, text="Add Student", command=open_add_student_form).pack(pady=10)
tk.Button(root, text="Add Subject", command=open_add_subject_form).pack(pady=10)
tk.Button(root, text="Import From Excel", command=open_import_excel_form).pack(pady=10)
tk.Button(root, text="View Transcript", command=open_view_transcript_form).pack(pady=10)
tk.Button(root, text="Exit", command=root.quit).pack(pady=10)  # Button to close the application

# Start the Tkinter event loop
root.mainloop()
