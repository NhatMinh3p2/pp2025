class Student:
    def __init__(self, sid="", name="", dob=""):
        self.__id = sid
        self.__name = name
        self.__dob = dob

    def get_id(self): return self.__id
    def get_name(self): return self.__name
    def get_dob(self): return self.__dob

    def input_info(self):
        self.__id = input("Student ID: ")
        self.__name = input("Student Name: ")
        self.__dob = input("DoB (dd/mm/yyyy): ")

    def __str__(self):
        return f"{self.__id:<10} {self.__name:<20} {self.__dob}"