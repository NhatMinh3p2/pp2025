class Course:
    def __init__(self, cid="", name="", credits=0):
        self.__id = cid
        self.__name = name
        self.__credits = credits

    def get_id(self): return self.__id
    def get_name(self): return self.__name
    def get_credits(self): return self.__credits

    def input_info(self):
        self.__id = input("Course ID: ")
        self.__name = input("Course Name: ")
        while True:
            try:
                cr = int(input("Credits (1-5): "))
                if 1 <= cr <= 5:
                    self.__credits = cr
                    break
                print("Credits must be 1-5.")
            except:
                print("Invalid number.")

    def __str__(self):
        return f"{self.__id:<8} {self.__name:<25} {self.__credits} cr"