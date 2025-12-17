import tkinter as tk
from tkinter import ttk
import numpy as np

class GPATab:
    def __init__(self, notebook, students, courses, marks):
        self.students = students
        self.courses = courses
        self.marks = marks

        self.frame = ttk.Frame(notebook)
        self.setup_ui()

    def setup_ui(self):
        header = ttk.Label(self.frame, text="Student GPA Ranking (Weighted by Credits)", font=("Helvetica", 14, "bold"))
        header.pack(pady=20)

        refresh_btn = ttk.Button(self.frame, text="Refresh GPA Ranking", command=self.calculate_gpa)
        refresh_btn.pack(pady=10)

        table_frame = ttk.Frame(self.frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("Rank", "Student ID", "Name", "GPA")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)
        for i, col in enumerate(columns):
            self.tree.heading(col, text=col)
            width = 100 if i == 0 else 200
            self.tree.column(col, width=width, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.calculate_gpa()

    def calculate_gpa(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.students or not self.courses:
            self.tree.insert("", "end", values=("—", "No data", "", ""))
            return

        gpa_list = []
        for stu in self.students:
            total_weighted = 0.0
            total_credits = 0

            for course in self.courses:
                cid = course.get_id()
                credit = course.get_credits()
                mark_obj = next((m for m in self.marks.get(cid, []) if m.get_student_id() == stu.get_id()), None)
                if mark_obj:
                    total_weighted += mark_obj.get_mark() * credit
                    total_credits += credit

            gpa = round(total_weighted / total_credits, 2) if total_credits > 0 else 0.0
            gpa_list.append((stu, gpa))

        gpa_list.sort(key=lambda x: x[1], reverse=True)

        for rank, (stu, gpa) in enumerate(gpa_list, 1):
            self.tree.insert("", "end", values=(rank, stu.get_id(), stu.get_name(), f"{gpa:.2f}"))