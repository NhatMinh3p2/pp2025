class Student:
    def __init__(self, sid, name, dob):
        self.__id = sid
        self.__name = name
        self.__dob = dob

    
    def get_id(self): return self.__id
    def get_name(self): return self.__name
    def get_dob(self): return self.__dob

    def list(self):
        print(f"ID: {self.__id}, Name: {self.__name}, DoB: {self.__dob}")


class Course:
    def __init__(self, cid, name):
        self.__id = cid
        self.__name = name

    def get_id(self): return self.__id
    def get_name(self): return self.__name

    def list(self):
        print(f"ID: {self.__id}, Name: {self.__name}")


class Mark:
    def __init__(self):
        self.__marks = {} 

    def input(self, course, students):
        cid = course.get_id()
        if cid not in self.__marks:
            self.__marks[cid] = {}

        print(f"Entering marks for course: {course.get_name()} ({cid})")
        for s in students:
            sid = s.get_id()
            mark = float(input(f"Mark for {s.get_name()} ({sid}): "))
            self.__marks[cid][sid] = mark
        print()

    def list(self, course, students):
        cid = course.get_id()
        if cid not in self.__marks:
            print("No marks for this course.")
            return

        print(f"--- Marks for course {course.get_name()} ({cid}) ---")
        for s in students:
            sid = s.get_id()
            mark = self.__marks[cid].get(sid, "N/A")
            print(f"{s.get_name()} ({sid}): {mark}")
        print()


class StudentManagement:
    def __init__(self):
        self.__students = []

    def input(self):
        n = int(input("Enter number of students: "))
        for _ in range(n):
            sid = input("Student ID: ")
            name = input("Student Name: ")
            dob = input("Student DoB: ")
            self.__students.append(Student(sid, name, dob))
        print()

    def list(self):
        print("--- Student List ---")
        for s in self.__students:
            s.list()
        print()

    def get_all(self): return self.__students


class CourseManagement:
    def __init__(self):
        self.__courses = []

    def input(self):
        c = int(input("Enter number of courses: "))
        for _ in range(c):
            cid = input("Course ID: ")
            name = input("Course Name: ")
            self.__courses.append(Course(cid, name))
        print()

    def list(self):
        print("--- Course List ---")
        for c in self.__courses:
            c.list()
        print()

    def get(self, cid):
        for c in self.__courses:
            if c.get_id() == cid:
                return c
        return None

    def get_all(self): return self.__courses



class StudentMarkSystem:
    def __init__(self):
        self.students = StudentManagement()
        self.courses = CourseManagement()
        self.marks = Mark()

    def run(self):
        self.students.input()
        self.courses.input()

        while True:
            print("Options:")
            print("1. List students")
            print("2. List courses")
            print("3. Input marks for a course")
            print("4. Show marks for a course")
            print("0. Exit")

            choice = input("Your choice: ")
            if choice == "1":
                self.students.list()
            elif choice == "2":
                self.courses.list()
            elif choice == "3":
                cid = input("Enter course ID: ")
                course = self.courses.get(cid)
                if course:
                    self.marks.input(course, self.students.get_all())
                else:
                    print("Course not found!\n")
            elif choice == "4":
                cid = input("Enter course ID: ")
                course = self.courses.get(cid)
                if course:
                    self.marks.list(course, self.students.get_all())
                else:
                    print("Course not found!\n")
            elif choice == "0":
                break
            else:
                print("Invalid choice! Try again.\n")


if __name__ == "__main__":
    sms = StudentMarkSystem()
    sms.run()
