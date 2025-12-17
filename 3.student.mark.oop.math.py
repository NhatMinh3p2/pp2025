# File: 3.student.mark.oop.math.py
import math
import numpy as np
import curses
from curses import wrapper

class Student:
    def __init__(self, sid="", name="", dob=""):
        self.__id = sid     
        self.__name = name
        self.__dob = dob

    def get_id(self): return self.__id
    def get_name(self): return self.__name
    def get_dob(self): return self.__dob

    def input(self):
        self.__id = input("Student ID: ")
        self.__name = input("Student Name: ")
        self.__dob = input("DoB (dd/mm/yyyy): ")

    def display(self):
        print(f"ID: {self.__id:<8} Name: {self.__name:<20} DoB: {self.__dob}")

    def __str__(self):
        return f"Student({self.__id}, {self.__name})"


class Course:
    def __init__(self, cid="", name="", credits=0):
        self.__id = cid
        self.__name = name
        self.__credits = credits  # Added credits

    def get_id(self): return self.__id
    def get_name(self): return self.__name
    def get_credits(self): return self.__credits

    def input(self):
        self.__id = input("Course ID: ")
        self.__name = input("Course Name: ")
        while True:
            try:
                self.__credits = int(input("Credits (1-5): "))
                if 1 <= self.__credits <= 5:
                    break
                else:
                    print("Credits should be 1-5.")
            except:
                print("Enter a valid number.")

    def display(self):
        print(f"ID: {self.__id:<8} Name: {self.__name:<25} Credits: {self.__credits}")

    def __str__(self):
        return f"Course({self.__id}, {self.__name}, {self.__credits}cr)"


class Mark:
    def __init__(self, student_id="", course_id="", mark=0.0):
        self.__student_id = student_id
        self.__course_id = course_id
        self.__mark = math.floor(mark * 10) / 10.0  # Floor to 1 decimal

    def get_student_id(self): return self.__student_id
    def get_course_id(self): return self.__course_id
    def get_mark(self): return self.__mark

    def set_mark(self, mark):
        if 0 <= mark <= 20:  # Allow input 0-20, then convert to 0-10 scale if needed
            scaled = mark / 2.0 if mark > 10 else mark
            self.__mark = math.floor(scaled * 10) / 10.0
        else:
            print("  Warning: Mark should be 0-20. Stored as is.")
            self.__mark = math.floor(mark * 10) / 10.0

    def input_mark(self, student_name):
        while True:
            try:
                m = float(input(f"  Mark for {student_name} (0-20): "))
                self.set_mark(m)
                break
            except:
                print("  Invalid input! Enter a number.")

    def display(self):
        print(f"  Student ID: {self.__student_id:<8} Mark: {self.__mark:.1f}")

    def __str__(self):
        return f"Mark({self.__student_id}, {self.__course_id}, {self.__mark:.1f})"


class MarkManagement:
    def __init__(self):
        self.__students = []
        self.__courses = []
        self.__marks = {}  # course_id -> list of Mark objects

    # === Input Methods ===
    def input_students(self):
        n = int(input("Enter number of students: "))
        for i in range(n):
            print(f"\nStudent {i+1}/{n}")
            s = Student()
            s.input()
            self.__students.append(s)

    def input_courses(self):
        n = int(input("Enter number of courses: "))
        for i in range(n):
            print(f"\nCourse {i+1}/{n}")
            c = Course()
            c.input()
            self.__courses.append(c)
            self.__marks[c.get_id()] = []

    def input_marks(self):
        if not self.__courses:
            print("Add courses first!")
            return
        self.list_courses()
        cid = input("\nSelect course ID to input marks: ")
        if cid not in self.__marks:
            print("Invalid course ID!")
            return

        print(f"\nInputting marks for course: {self._find_course_name(cid)}")
        for s in self.__students:
            m = Mark(s.get_id(), cid)
            m.input_mark(s.get_name())
            self.__marks[cid].append(m)

    # === Listing ===
    def list_students(self):
        print("\n=== List of Students ===")
        if not self.__students:
            print("No students.")
            return
        print(f"{'ID':<10} {'Name':<20} {'DoB':<12}")
        print("-" * 50)
        for s in self.__students:
            print(f"{s.get_id():<10} {s.get_name():<20} {s.get_dob():<12}")

    def list_courses(self):
        print("\n=== List of Courses ===")
        if not self.__courses:
            print("No courses.")
            return
        print(f"{'ID':<8} {'Name':<25} {'Credits'}")
        print("-" * 45)
        for c in self.__courses:
            c.display()

    def show_marks_for_course(self):
        self.list_courses()
        cid = input("\nSelect course to view marks: ")
        if cid not in self.__marks or not self.__marks[cid]:
            print("No marks for this course.")
            return
        cname = self._find_course_name(cid)
        print(f"\n=== Marks for {cname} ({cid}) ===")
        print(f"{'Student ID':<12} {'Name':<20} {'Mark':<6}")
        print("-" * 40)
        for m in self.__marks[cid]:
            stu = self._find_student_by_id(m.get_student_id())
            print(f"{m.get_student_id():<12} {stu.get_name():<20} {m.get_mark():.1f}")

    # === GPA Calculation using NumPy ===
    def calculate_gpa(self):
        if not self.__students or not self.__courses:
            print("Need students and courses with marks!")
            return

        gpa_list = []
        for student in self.__students:
            marks = []
            credits = []
            total_credit = 0

            for course in self.__courses:
                cid = course.get_id()
                credit = course.get_credits()
                mark_obj = next((m for m in self.__marks.get(cid, []) if m.get_student_id() == student.get_id()), None)
                if mark_obj:
                    marks.append(mark_obj.get_mark())
                    credits.append(credit)
                    total_credit += credit

            if total_credit == 0:
                gpa = 0.0
            else:
                # Weighted average using numpy
                marks_arr = np.array(marks)
                credits_arr = np.array(credits)
                weighted_sum = np.sum(marks_arr * credits_arr)
                gpa = weighted_sum / total_credit
                gpa = round(gpa, 2)

            gpa_list.append((student, gpa))

        # Sort by GPA descending
        gpa_list.sort(key=lambda x: x[1], reverse=True)

        # Display sorted GPA
        print("\n" + "="*60)
        print("STUDENTS RANKED BY GPA (DESCENDING)".center(60))
        print("="*60)
        print(f"{'Rank':<5} {'ID':<10} {'Name':<20} {'GPA':<6}")
        print("-" * 60)
        for i, (stu, gpa) in enumerate(gpa_list, 1):
            print(f"{i:<5} {stu.get_id():<10} {stu.get_name():<20} {gpa:<6}")

    # === Helpers ===
    def _find_course_name(self, cid):
        for c in self.__courses:
            if c.get_id() == cid:
                return c.get_name()
        return "Unknown"

    def _find_student_by_id(self, sid):
        for s in self.__students:
            if s.get_id() == sid:
                return s
        return None

    # === Main Menu with Curses ===
    def run_with_curses(self, stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

        menu = [
            "Input Students",
            "Input Courses",
            "Input Marks for a Course",
            "List Students",
            "List Courses",
            "Show Marks for a Course",
            "Show Student GPA Ranking",
            "Exit"
        ]

        current = 0
        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            title = "OOP STUDENT MARK MANAGEMENT SYSTEM - PRACTICAL 3"
            stdscr.addstr(1, w//2 - len(title)//2, title, curses.color_pair(1) | curses.A_BOLD)

            for idx, item in enumerate(menu):
                x = w//2 - len(item)//2
                y = h//2 - len(menu)//2 + idx
                if idx == current:
                    stdscr.attron(curses.color_pair(2) | curses.A_REVERSE)
                    stdscr.addstr(y, x, item)
                    stdscr.attroff(curses.color_pair(2) | curses.A_REVERSE)
                else:
                    stdscr.addstr(y, x, item, curses.color_pair(3))

            stdscr.refresh()

            key = stdscr.getch()
            if key == curses.KEY_UP and current > 0:
                current -= 1
            elif key == curses.KEY_DOWN and current < len(menu)-1:
                current += 1
            elif key in [10, 13]:  # Enter
                stdscr.clear()
                if current == 0:
                    stdscr.addstr(0, 0, ">>> Input Students <<<")
                    stdscr.refresh()
                    curses.echo()
                    self.input_students()
                    curses.noecho()
                elif current == 1:
                    stdscr.addstr(0, 0, ">>> Input Courses <<<")
                    stdscr.refresh()
                    curses.echo()
                    self.input_courses()
                    curses.noecho()
                elif current == 2:
                    stdscr.addstr(0, 0, ">>> Input Marks <<<")
                    stdscr.refresh()
                    curses.echo()
                    self.input_marks()
                    curses.noecho()
                elif current == 3:
                    self.list_students()
                elif current == 4:
                    self.list_courses()
                elif current == 5:
                    self.show_marks_for_course()
                elif current == 6:
                    self.calculate_gpa()
                elif current == 7:
                    stdscr.addstr(h//2, w//2 - 15, "Thank You! Goodbye!", curses.color_pair(4) | curses.A_BOLD)
                    stdscr.refresh()
                    curses.napms(1500)
                    break

                stdscr.addstr(h-2, 0, "Press any key to continue...")
                stdscr.refresh()
                stdscr.getch()

    def run(self):
        print("Launching...")
        wrapper(self.run_with_curses)


if __name__ == "__main__":
    system = MarkManagement()
    system.run()