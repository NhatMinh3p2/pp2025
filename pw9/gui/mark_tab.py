import tkinter as tk
from tkinter import ttk, messagebox
from domains import Mark
import math
from persistence import save_all_async

class MarkTab:
    def __init__(self, notebook, students, courses, marks):
        self.students = students
        self.courses = courses
        self.marks = marks

        self.frame = ttk.Frame(notebook)
        self.setup_ui()

    def setup_ui(self):
        top = ttk.Frame(self.frame)
        top.pack(padx=20, pady=20, fill="x")

        ttk.Label(top, text="Select Course:").pack(side="left")
        self.course_var = tk.StringVar()
        self.course_combo = ttk.Combobox(top, textvariable=self.course_var, state="readonly", width=30)
        self.course_combo.pack(side="left", padx=10)
        self.course_combo.bind("<<ComboboxSelected>>", lambda e: self.load_marks())

        refresh_btn = ttk.Button(top, text="Refresh", command=self.refresh_courses)
        refresh_btn.pack(side="left")

        # Marks Table
        table_frame = ttk.LabelFrame(self.frame, text=" Student Marks ", padding=10)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("Student ID", "Name", "Mark (0-10)")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        # Edit mark on double-click
        self.tree.bind("<Double-1>", self.edit_mark)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.refresh_courses()

    def refresh_courses(self):
        courses_list = [f"{c.get_id()} - {c.get_name()}" for c in self.courses]
        self.course_combo['values'] = courses_list
        if courses_list:
            self.course_combo.current(0)
            self.load_marks()

    def load_marks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.courses:
            return

        selected = self.course_var.get()
        if not selected:
            return
        course_id = selected.split(" - ")[0]

        course_marks = self.marks.get(course_id, [])
        mark_dict = {m.get_student_id(): m.get_mark() for m in course_marks}

        for s in self.students:
            mark = mark_dict.get(s.get_id(), "")
            self.tree.insert("", "end", values=(s.get_id(), s.get_name(), f"{mark:.1f}" if mark else ""))

    def edit_mark(self, event):
        item = self.tree.selection()
        if not item:
            return
        student_id = self.tree.item(item, "values")[0]

        selected = self.course_var.get()
        if not selected:
            return
        course_id = selected.split(" - ")[0]

        current_mark = ""
        for m in self.marks.get(course_id, []):
            if m.get_student_id() == student_id:
                current_mark = str(m.get_mark())
                break

        new_mark = tk.simpledialog.askstring("Input Mark", f"Enter mark for {student_id} (0-20):", initialvalue=current_mark)
        if new_mark is None:
            return

        try:
            val = float(new_mark)
            if not (0 <= val <= 20):
                raise ValueError
            scaled = val / 2.0 if val > 10 else val
            final_mark = math.floor(scaled * 10) / 10.0
        except:
            messagebox.showerror("Error", "Mark must be 0–20!")
            return

        # Update or add mark
        found = False
        for m in self.marks[course_id]:
            if m.get_student_id() == student_id:
                m._Mark__mark = final_mark  # direct access (private, but works)
                found = True
                break
        if not found:
            new_m = Mark(student_id, course_id, final_mark)
            new_m._Mark__mark = final_mark
            self.marks[course_id].append(new_m)

        save_all_async(self.students, self.courses, self.marks)
        self.load_marks()
        messagebox.showinfo("Success", f"Mark updated: {final_mark:.1f}")