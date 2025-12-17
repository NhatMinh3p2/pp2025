import math

class Mark:
    def __init__(self, student_id="", course_id="", mark=0.0):
        self.__student_id = student_id
        self.__course_id = course_id
        self.__mark = math.floor(mark * 10) / 10.0

    def get_student_id(self): return self.__student_id
    def get_course_id(self): return self.__course_id
    def get_mark(self): return self.__mark

    def input_mark(self, student_name):
        while True:
            try:
                m = float(input(f"  Mark for {student_name} (0-20): "))
                scaled = m / 2.0 if m > 10 else m
                self.__mark = math.floor(scaled * 10) / 10.0
                break
            except:
                print("  Please enter a valid number.")

    def __str__(self):
        return f"{self.__student_id:<12} {self.__mark:.1f}"