import tkinter as tk
from tkinter import ttk, messagebox
from domains import Course
from persistence import save_all_async

class CourseTab:
    def __init__(self, notebook, students, courses, marks):
        self.students = students
        self.courses = courses
        self.marks = marks

        self.frame = ttk.Frame(notebook)
        self.setup_ui()

    def setup_ui(self):
        # Input Form
        form = ttk.LabelFrame(self.frame, text=" Add New Course ", padding=15)
        form.pack(padx=20, pady=20, fill="x")

        ttk.Label(form, text="Course ID:").grid(row=0, column=0, sticky="w", pady=5)
        self.id_entry = ttk.Entry(form, width=30)
        self.id_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(form, text="Course Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(form, width=30)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(form, text="Credits (1-5):").grid(row=2, column=0, sticky="w", pady=5)
        self.credits_entry = ttk.Entry(form, width=30)
        self.credits_entry.grid(row=2, column=1, padx=10, pady=5)

        add_btn = ttk.Button(form, text="Add Course", command=self.add_course)
        add_btn.grid(row=3, column=1, pady=15, sticky="e")

        # Course List
        list_frame = ttk.LabelFrame(self.frame, text=" Course List ", padding=10)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Name", "Credits")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.refresh_list()

    def add_course(self):
        cid = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        try:
            credits = int(self.credits_entry.get().strip())
            if not (1 <= credits <= 5):
                raise ValueError
        except:
            messagebox.showerror("Error", "Credits must be 1–5!")
            return

        if not (cid and name):
            messagebox.showerror("Error", "All fields required!")
            return

        if any(c.get_id() == cid for c in self.courses):
            messagebox.showerror("Error", "Course ID already exists!")
            return

        course = Course(cid, name, credits)
        self.courses.append(course)
        self.marks[cid] = []  # initialize mark list
        self.refresh_list()

        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.credits_entry.delete(0, tk.END)

        save_all_async(self.students, self.courses, self.marks)
        messagebox.showinfo("Success", "Course added & auto-saved!")

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for c in self.courses:
            self.tree.insert("", "end", values=(c.get_id(), c.get_name(), c.get_credits()))