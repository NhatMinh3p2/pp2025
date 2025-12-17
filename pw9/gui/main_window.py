import tkinter as tk
from tkinter import ttk
from .student_tab import StudentTab
from .course_tab import CourseTab
from .mark_tab import MarkTab
from .gpa_tab import GPATab

class MainWindow:
    def __init__(self, root, students, courses, marks):
        self.root = root
        self.students = students
        self.courses = courses
        self.marks = marks

        # Header
        header = tk.Frame(root, bg="#2c3e50", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header, text="Student Mark Management System",
            font=("Helvetica", 20, "bold"), fg="white", bg="#2c3e50"
        )
        title.pack(pady=20)

        subtitle = tk.Label(
            header, text="Practical Work 9 – GUI with Tkinter + Auto-Save",
            font=("Helvetica", 10), fg="#bdc3c7", bg="#2c3e50"
        )
        subtitle.pack()

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        # Create tabs
        self.student_tab = StudentTab(self.notebook, self.students, self.courses, self.marks)
        self.course_tab = CourseTab(self.notebook, self.students, self.courses, self.marks)
        self.mark_tab = MarkTab(self.notebook, self.students, self.courses, self.marks)
        self.gpa_tab = GPATab(self.notebook, self.students, self.courses, self.marks)

        self.notebook.add(self.student_tab.frame, text="  Students  ")
        self.notebook.add(self.course_tab.frame, text="  Courses  ")
        self.notebook.add(self.mark_tab.frame, text="  Marks  ")
        self.notebook.add(self.gpa_tab.frame, text="  GPA Ranking  ")

        # Status bar
        self.status = tk.Label(
            root, text="Ready | Auto-saving in background...", 
            relief="sunken", anchor="w", bg="#ecf0f1", fg="#2c3e50"
        )
        self.status.pack(side="bottom", fill="x")