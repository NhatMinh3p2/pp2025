from domains import Student, Course, Mark

def input_students(students_list):
    print("\n--- Input Students ---")
    n = int(input("Number of students: "))
    for i in range(n):
        print(f"\nStudent {i+1}/{n}")
        s = Student()
        s.input_info()
        students_list.append(s)

def input_courses(courses_list, marks_dict):
    print("\n--- Input Courses ---")
    n = int(input("Number of courses: "))
    for i in range(n):
        print(f"\nCourse {i+1}/{n}")
        c = Course()
        c.input_info()
        courses_list.append(c)
        marks_dict[c.get_id()] = []

def input_marks(students_list, courses_list, marks_dict):
    if not courses_list:
        print("No courses available!")
        return
    print("\nAvailable courses:")
    for c in courses_list:
        print("  ", c)
    cid = input("\nEnter course ID to input marks: ")
    if cid not in marks_dict:
        print("Invalid course ID!")
        return

    print(f"\nEntering marks for: {next(c.get_name() for c in courses_list if c.get_id() == cid)}")
    for s in students_list:
        m = Mark(s.get_id(), cid)
        m.input_mark(s.get_name())
        marks_dict[cid].append(m)