import tkinter as tk
from tkinter import ttk
from persistence import load_all, start_background_saver
from gui.main_window import MainWindow

def main():
    start_background_saver()

    students, courses, marks = load_all()

    root = tk.Tk()
    root.title("Student Mark Management System - Practical 9")
    root.geometry("1100x700")
    root.configure(bg="#f0f0f0")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TNotebook", background="#f0f0f0")
    style.configure("TNotebook.Tab", padding=[15, 8], font=('Helvetica', 11))

    app = MainWindow(root, students, courses, marks)
    root.mainloop()

    from persistence import save_all_sync, shutdown_saver
    save_all_sync(students, courses, marks)
    shutdown_saver()
    print("GUI closed. All data saved.")

if __name__ == "__main__":
    main()