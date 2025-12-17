import curses
from input import input_students, input_courses, input_marks
from output import (
    display_students, display_courses,
    show_marks, calculate_and_show_gpa
)
from domains import Student, Course

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

    students = []
    courses = []
    marks = {}

    menu = [
        "1. Add Students",
        "2. Add Courses",
        "3. Input Marks",
        "4. List Students",
        "5. List Courses",
        "6. Show Marks for Course",
        "7. Show GPA Ranking",
        "8. Exit"
    ]

    current = 0
    while True:
        stdscr.clear()
        title = "STUDENT MARK MANAGEMENT - PRACTICAL 4"
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
                input_courses(courses, marks)
                curses.noecho()
            elif current == 2:
                curses.echo()
                input_marks(students, courses, marks)
                curses.noecho()
            elif current == 3:
                display_students(stdscr, students)
            elif current == 4:
                display_courses(stdscr, courses)
            elif current == 5:
                show_marks(stdscr, students, courses, marks)
            elif current == 6:
                calculate_and_show_gpa(stdscr, students, courses, marks)
            elif current == 7:
                stdscr.clear()
                stdscr.addstr(10, 15, "Thank You! See you again!", curses.color_pair(4) | curses.A_BOLD)
                stdscr.refresh()
                curses.napms(2000)
                break

if __name__ == "__main__":
    print("Starting Practical Work 4 - Modularized Version")
    curses.wrapper(main)