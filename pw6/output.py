import curses
import numpy as np
from curses import wrapper

def display_students(stdscr, students):
    stdscr.clear()
    stdscr.addstr(0, 0, "=== LIST OF STUDENTS ===\n", curses.A_BOLD)
    stdscr.addstr(f"{'ID':<10} {'Name':<20} {'DoB':<12}\n")
    stdscr.addstr("-" * 50 + "\n")
    for s in students:
        stdscr.addstr(f"{s}\n")
    stdscr.addstr("\nPress any key to continue...")
    stdscr.getch()

def display_courses(stdscr, courses):
    stdscr.clear()
    stdscr.addstr(0, 0, "=== LIST OF COURSES ===\n", curses.A_BOLD)
    stdscr.addstr(f"{'ID':<8} {'Name':<25} {'Credits'}\n")
    stdscr.addstr("-" * 45 + "\n")
    for c in courses:
        stdscr.addstr(f"{c}\n")
    stdscr.addstr("\nPress any key...")
    stdscr.getch()

def show_marks(stdscr, students, courses, marks_dict):
    stdscr.clear()
    stdscr.addstr(0, 0, "Available courses:\n")
    for c in courses:
        stdscr.addstr(f"  {c.get_id()} - {c.get_name()}\n")
    cid = stdscr.getstr(20).decode().strip()
    if cid not in marks_dict or not marks_dict[cid]:
        stdscr.addstr(22, 0, "No marks for this course!")
        stdscr.getch()
        return

    cname = next(c.get_name() for c in courses if c.get_id() == cid)
    stdscr.clear()
    stdscr.addstr(0, 0, f"=== MARKS FOR {cname.upper()} ({cid}) ===\n", curses.A_BOLD)
    stdscr.addstr(f"{'Student ID':<12} {'Name':<20} {'Mark':<6}\n")
    stdscr.addstr("-" * 40 + "\n")
    for m in marks_dict[cid]:
        stu = next(s for s in students if s.get_id() == m.get_student_id())
        stdscr.addstr(f"{m.get_student_id():<12} {stu.get_name():<20} {m.get_mark():.1f}\n")
    stdscr.addstr("\nPress any key...")
    stdscr.getch()

def calculate_and_show_gpa(stdscr, students, courses, marks_dict):
    stdscr.clear()
    gpa_list = []
    for stu in students:
        marks = []
        credits = []
        total_cr = 0
        for course in courses:
            cid = course.get_id()
            mark_obj = next((m for m in marks_dict.get(cid, []) if m.get_student_id() == stu.get_id()), None)
            if mark_obj:
                marks.append(mark_obj.get_mark())
                credits.append(course.get_credits())
                total_cr += course.get_credits()
        if total_cr > 0:
            gpa = np.sum(np.array(marks) * np.array(credits)) / total_cr
            gpa = round(gpa, 2)
        else:
            gpa = 0.0
        gpa_list.append((stu, gpa))

    gpa_list.sort(key=lambda x: x[1], reverse=True)

    stdscr.addstr(0, 0, "STUDENTS RANKED BY GPA (DESCENDING)".center(60), curses.A_BOLD | curses.A_UNDERLINE)
    stdscr.addstr(2, 0, f"{'Rank':<5} {'ID':<10} {'Name':<20} {'GPA':<6}\n")
    stdscr.addstr("-" * 50 + "\n")
    for i, (stu, gpa) in enumerate(gpa_list, 1):
        stdscr.addstr(f"{i:<5} {stu.get_id():<10} {stu.get_name():<20} {gpa:<6}\n")
    stdscr.addstr("\nPress any key to return...")
    stdscr.getch()