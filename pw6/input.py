from domains import Student, Course, Mark
from persistence import save_all

def input_students(students_list, courses_list, marks_dict):
    print("\n--- Input Students ---")
    n = int(input("Number of students: "))
    for i in range(n):
        print(f"\nStudent {i+1}/{n}")
        s = Student()
        s.input_info()
        students_list.append(s)
    save_all(students_list, courses_list, marks_dict)

def input_courses(students_list, courses_list, marks_dict):
    print("\n--- Input Courses ---")
    n = int(input("Number of courses: "))
    for i in range(n):
        print(f"\nCourse {i+1}/{n}")
        c = Course()
        c.input_info()
        courses_list.append(c)
        marks_dict[c.get_id()] = []
    save_all(students_list, courses_list, marks_dict)

def input_marks(students_list, courses_list, marks_dict):
    if not courses_list:
        print("No courses! Add courses first.")
        return
    print("\nCourses:")
    for c in courses_list:
        print(f"  {c.get_id()} - {c.get_name()}")
    cid = input("\nEnter course ID: ")
    if cid not in marks_dict:
        print("Invalid course!")
        return

    cname = next(c.get_name() for c in courses_list if c.get_id() == cid)
    print(f"\nEntering marks for: {cname}")

    for s in students_list:
        m = Mark(s.get_id(), cid)
        m.input_mark(s.get_name())
        marks_dict[cid].append(m)

    save_all(students_list, courses_list, marks_dict)
    print("Marks saved!")