import tkinter as tk
from tkinter import ttk, messagebox
from domains import Student
from persistence import save_all_async

class StudentTab:
    def __init__(self, notebook, students, courses, marks):
        self.students = students
        self.courses = courses
        self.marks = marks

        self.frame = ttk.Frame(notebook)
        self.setup_ui()

    def setup_ui(self):
        # Input Form
        form = ttk.LabelFrame(self.frame, text=" Add New Student ", padding=15)
        form.pack(padx=20, pady=20, fill="x")

        ttk.Label(form, text="ID:").grid(row=0, column=0, sticky="w", pady=5)
        self.id_entry = ttk.Entry(form, width=30)
        self.id_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(form, text="Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(form, width=30)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(form, text="DoB (dd/mm/yyyy):").grid(row=2, column=0, sticky="w", pady=5)
        self.dob_entry = ttk.Entry(form, width=30)
        self.dob_entry.grid(row=2, column=1, padx=10, pady=5)

        add_btn = ttk.Button(form, text="Add Student", command=self.add_student)
        add_btn.grid(row=3, column=1, pady=15, sticky="e")

        # List
        list_frame = ttk.LabelFrame(self.frame, text=" Student List ", padding=10)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Name", "Date of Birth")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.refresh_list()

    def add_student(self):
        sid = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        dob = self.dob_entry.get().strip()

        if not (sid and name and dob):
            messagebox.showerror("Error", "All fields required!")
            return

        if any(s.get_id() == sid for s in self.students):
            messagebox.showerror("Error", "Student ID already exists!")
            return

        student = Student(sid, name, dob)
        self.students.append(student)
        self.refresh_list()
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)

        save_all_async(self.students, self.courses, self.marks)
        messagebox.showinfo("Success", "Student added & saved automatically!")

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for s in self.students:
            self.tree.insert("", "end", values=(s.get_id(), s.get_name(), s.get_dob()))