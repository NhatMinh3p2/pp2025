import curses
import os
from persistence import load_all, save_all_async, save_all_sync, start_background_saver, shutdown_saver
from input import input_students, input_courses, input_marks
from output import display_students, display_courses, show_marks, calculate_and_show_gpa

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)

    start_background_saver()

    students, courses, marks = load_all()

    stdscr.clear()
    stdscr.attron(curses.color_pair(5) | curses.A_BOLD)
    stdscr.addstr(5, 10, " PRACTICAL WORK 8 ", curses.A_REVERSE)
    stdscr.addstr(7, 8, " Multithreaded Auto-Save System ")
    stdscr.addstr(9, 12, " All changes saved in background! ")
    stdscr.attroff(curses.color_pair(5))
    stdscr.getch()

    menu = [
        "1. Add Students",
        "2. Add Courses",
        "3. Input Marks",
        "4. List Students",
        "5. List Courses",
        "6. Show Marks",
        "7. Show GPA Ranking",
        "8. Exit"
    ]

    cur = 0
    while True:
        stdscr.clear()
        stdscr.addstr(1, 2, "PW8 - MULTITHREADED PERSISTENCE", curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(2, 2, "Auto-save running in background", curses.color_pair(3))

        for i, item in enumerate(menu):
            if i == cur:
                stdscr.addstr(5+i, 4, f"→ {item}", curses.A_REVERSE | curses.color_pair(2))
            else:
                stdscr.addstr(5+i, 6, item, curses.color_pair(3))

        key = stdscr.getch()
        if key == curses.KEY_UP and cur > 0: cur -= 1
        elif key == curses.KEY_DOWN and cur < len(menu)-1: cur += 1
        elif key in [10, 13]:
            if cur == 0:
                curses.echo(); input_students(students, courses, marks); curses.noecho()
            elif cur == 1:
                curses.echo(); input_courses(students, courses, marks); curses.noecho()
            elif cur == 2:
                curses.echo(); input_marks(students, courses, marks); curses.noecho()
            elif cur == 3: display_students(stdscr, students)
            elif cur == 4: display_courses(stdscr, courses)
            elif cur == 5: show_marks(stdscr, students, courses, marks)
            elif cur == 6: calculate_and_show_gpa(stdscr, students, courses, marks)
            elif cur == 7:
                stdscr.clear()
                stdscr.addstr(10, 15, "FINAL SYNC SAVE...", curses.color_pair(4) | curses.A_BOLD)
                stdscr.refresh()
                save_all_sync(students, courses, marks)
                shutdown_saver()
                stdscr.addstr(12, 18, "Goodbye! All data safe.", curses.A_BOLD)
                stdscr.refresh()
                curses.napms(2000)
                break

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    curses.wrapper(main)