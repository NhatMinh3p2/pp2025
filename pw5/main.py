import curses
import os
from domains import Student, Course, Mark
from loader import load_data, save_data
from input import input_students, input_courses, input_marks
from output import (
    display_students, display_courses,
    show_marks, calculate_and_show_gpa
)

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)


    students, courses, marks = load_data(Student, Course, Mark)

    if students is None:
        students = []
        courses = []
        marks = {}

    stdscr.clear()
    stdscr.addstr(5, 10, "STUDENT MARK MANAGEMENT - PRACTICAL 5", curses.A_BOLD | curses.color_pair(1))
    stdscr.addstr(7, 10, "Persistent Data + Compression", curses.color_pair(2))
    stdscr.addstr(9, 10, "Press any key to continue...", curses.color_pair(3))
    stdscr.getch()

    menu = [
        "1. Add Students",
        "2. Add Courses",
        "3. Input Marks",
        "4. List Students",
        "5. List Courses",
        "6. Show Marks for Course",
        "7. Show GPA Ranking",
        "8. Exit & Save"
    ]

    current = 0
    while True:
        stdscr.clear()
        title = "PRACTICAL 5 - PERSISTENT INFO"
        stdscr.addstr(1, 2, title, curses.color_pair(1) | curses.A_BOLD)

        for idx, item in enumerate(menu):
            y = 4 + idx
            if idx == current:
                stdscr.addstr(y, 4, "→ " + item, curses.A_REVERSE | curses.color_pair(2))
            else:
                stdscr.addstr(y, 6, item, curses.color_pair(3))

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current > 0:
            current -= 1
        elif key == curses.KEY_DOWN and current < len(menu)-1:
            current += 1
        elif key in [10, 13]:
            if current == 0:
                curses.echo()
                input_students(students)
                curses.noecho()
            elif current == 1:
                curses.echo()
                input_courses(courses, marks, students)
                curses.noecho()
            elif current == 2:
                curses.echo()
                input_marks(students, courses, marks, students)
                curses.noecho()
            elif current == 3:
                display_students(stdscr, students)
            elif current == 4:
                display_courses(stdscr, courses)
            elif current == 5:
                show_marks(stdscr, students, courses, marks)
            elif current == 6:
                calculate_and_show_gpa(stdscr, students, courses, marks)
            elif current == 7:  # EXIT
                stdscr.clear()
                stdscr.addstr(10, 15, "SAVING ALL DATA...", curses.color_pair(4))
                stdscr.refresh()
                save_data(students, courses, marks)
                stdscr.addstr(12, 15, "Goodbye! See you next time!", curses.A_BOLD)
                stdscr.refresh()
                curses.napms(2000)
                break

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    curses.wrapper(main)