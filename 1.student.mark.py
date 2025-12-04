students = []  
courses = []   
marks = {}     


def input_number_of_students():
    n = int(input("Enter number of students: "))
    return n

def input_student_info(n):
    for _ in range(n):
        sid = input("Student ID: ")
        name = input("Student Name: ")
        dob = input("Student DoB: ")
        students.append({"id": sid, "name": name, "dob": dob})
    print()

def input_number_of_courses():
    c = int(input("Enter number of courses: "))
    return c

def input_course_info(c):
    for _ in range(c):
        cid = input("Course ID: ")
        name = input("Course Name: ")
        courses.append({"id": cid, "name": name})
        marks[cid] = {}
    print()

def select_course_and_input_marks():
    cid = input("Enter course ID to input marks: ")
    if cid not in marks:
        print("Course not found!")
        return

    print(f"Entering marks for course: {cid}")
    for s in students:
        mark = float(input(f"Mark for {s['name']} ({s['id']}): "))
        marks[cid][s['id']] = mark
    print()


def list_courses():
    print("--- Course List ---")
    for c in courses:
        print(f"ID: {c['id']}, Name: {c['name']}")
    print()

def list_students():
    print("--- Student List ---")
    for s in students:
        print(f"ID: {s['id']}, Name: {s['name']}, DoB: {s['dob']}")
    print()

def show_student_marks():
    cid = input("Enter course ID to show marks: ")
    if cid not in marks:
        print("Course not found!")
        return

    print(f"--- Marks for course {cid} ---")
    for s in students:
        sid = s['id']
        mark = marks[cid].get(sid, "N/A")
        print(f"{s['name']} ({sid}): {mark}")
    print()


def main():
    n = input_number_of_students()
    input_student_info(n)

    c = input_number_of_courses()
    input_course_info(c)

    while True:
        print("Options:")
        print("1. List students")
        print("2. List courses")
        print("3. Input marks for a course")
        print("4. Show marks for a course")
        print("0. Exit")

        choice = input("Your choice: ")
        if choice == "1":
            list_students()
        elif choice == "2":
            list_courses()
        elif choice == "3":
            select_course_and_input_marks()
        elif choice == "4":
            show_student_marks()
        elif choice == "0":
            break
        else:
            print("Invalid choice! Try again.\n")

if __name__ == "__main__":
    main()
