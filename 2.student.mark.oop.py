class Student:
    def __init__(self, sid="", name="", dob=""):
        self.__id = sid     
        self.__name = name
        self.__dob = dob

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob


    def input(self):
        self.__id = input("Student ID:")
        self.__name = input("Student Name:")
        self.__dob = input("DoB (dd/mm/yyyy):")


    def display(self):
        print(f"ID: {self.__id:<8} Name: {self.__name:<20} DoB: {self.__dob}")

 
    def __str__(self):
        return f"Student({self.__id}, {self.__name})"


class Course:
    def __init__(self, cid="", name=""):
        self.__id = cid          # private
        self.__name = name


    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name


    def input(self):
        self.__id = input("Course ID:")
        self.__name = input("Course Name:")


    def display(self):
        print(f"ID: {self.__id:<8} Name: {self.__name:<20}")

    def __str__(self):
        return f"Course({self.__id}, {self.__name})"


class Mark:
    def __init__(self, student_id="", course_id="", mark=0.0):
        self.__student_id = student_id
        self.__course_id = course_id
        self.__mark = mark

    def get_student_id(self):
        return self.__student_id

    def get_course_id(self):
        return self.__course_id

    def get_mark(self):
        return self.__mark

    def set_mark(self, mark):
        if 0 <= mark <= 10:
            self.__mark = mark
        else:
            print("  Warning: Mark should be 0-10. Stored anyway.")


    def input_mark(self, student_name):
        while True:
            try:
                m = float(input(f"  Mark for {student_name}: "))
                self.set_mark(m)
                break
            except ValueError:
                print("  Invalid! Enter a number (0-10).")

    def display(self):
        print(f"  Student ID: {self.__student_id:<8} Mark: {self.__mark:<5}")

    def __str__(self):
        return f"Mark({self.__student_id}, {self.__course_id}, {self.__mark})"


class MarkManagement:
    def __init__(self):
        self.__students = []  
        self.__courses = []     
        self.__marks = {}       


    def input_students(self):
        print("\n--- Input Students ---")
        n = int(input("Enter number of students: "))
        for i in range(n):
            print(f"\nStudent {i+1}:")
            s = Student()
            s.input()
            self.__students.append(s)

    def input_courses(self):
        print("\n--- Input Courses ---")
        n = int(input("Enter number of courses: "))
        for i in range(n):
            print(f"\nCourse {i+1}:")
            c = Course()
            c.input()
            self.__courses.append(c)
            self.__marks[c.get_id()] = [] 

    def input_marks(self):
        if not self.__courses:
            print("No courses! Add courses first.")
            return

        print("\n--- Input Marks ---")
        self.list_courses() 
        course_id = input("\nSelect course ID to input marks: ")

        if course_id not in self.__marks:
            print("Invalid course ID!")
            return

        print(f"\nEntering marks for course: {self._find_course_name(course_id)}")
        for student in self.__students:
            mark = Mark(student.get_id(), course_id)
            mark.input_mark(student.get_name())
            self.__marks[course_id].append(mark)


    def list_courses(self):
        print("\n=== List of Courses ===")
        if not self.__courses:
            print("No courses.")
            return
        print(f"{'ID':<10} {'Name':<20}")
        print("-" * 30)
        for c in self.__courses:
            c.display()

    def list_students(self):
        print("\n=== List of Students ===")
        if not self.__students:
            print("No students.")
            return
        print(f"{'ID':<10} {'Name':<20} {'DoB':<12}")
        print("-" * 45)
        for s in self.__students:
            s.display()

    def show_marks_for_course(self):
        if not self.__courses:
            print("No courses available.")
            return

        self.list_courses()
        course_id = input("\nSelect course ID to view marks: ")
        if course_id not in self.__marks or not self.__marks[course_id]:
            print("No marks recorded for this course.")
            return

        course_name = self._find_course_name(course_id)
        print(f"\n=== Marks for {course_name} ({course_id}) ===")
        print(f"{'Student ID':<12} {'Name':<20} {'Mark':<6}")
        print("-" * 40)

        for mark in self.__marks[course_id]:
            student = self._find_student_by_id(mark.get_student_id())
            if student:
                print(f"{mark.get_student_id():<12} {student.get_name():<20} {mark.get_mark():<6}")




    def _find_course_name(self, course_id):
        for c in self.__courses:
            if c.get_id() == course_id:
                return c.get_name()
        return "Unknown"

    def _find_student_by_id(self, sid):
        for s in self.__students:
            if s.get_id() == sid:
                return s
        return None


    def run(self):
        print("=== OOP Student Mark Management System ===")
        self.input_students()
        self.input_courses()

        while True:
            print("\n" + "="*45)
            print("1. List all courses")
            print("2. List all students")
            print("3. Show marks for a course")
            print("4. Input marks for a course")
            print("5. Exit")
            print("="*45)
            choice = input("Choose (1-5): ")

            if choice == '1':
                self.list_courses()
            elif choice == '2':
                self.list_students()
            elif choice == '3':
                self.show_marks_for_course()
            elif choice == '4':
                self.input_marks()
            elif choice == '5':
                print("Bye!")
                break
            else:
                print("Invalid option! Try again.")





if __name__ == "__main__":
    system = MarkManagement()
    system.run()