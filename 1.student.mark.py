def main():
    print("=== Welcome to Student Mark Manager ===")
    
    
    num_students = int(input("Enter number of students in the class: "))
    students = []  # list to hold student info
    
   
    print("\n--- Enter Student Information ---")
    for i in range(num_students):
        print(f"\nStudent {i+1}:")
        sid = input("  ID: ")
        name = input("  Name: ")
        dob = input("  DoB (dd/mm/yyyy): ")
        
     
        students.append((sid, name, dob, {})) 
    
 
    num_courses = int(input("\nEnter number of courses: "))
    courses = []  
    

    print("\n--- Enter Course Information ---")
    for i in range(num_courses):
        cid = input(f"Course {i+1} ID: ")
        cname = input(f"Course {i+1} Name: ")
        courses.append((cid, cname))
    

    print("\n--- Input Marks ---")
    for cid, cname in courses:
        print(f"\nEntering marks for course: {cname} ({cid})")
        for j, (sid, sname, _, marks_dict) in enumerate(students):
            while True:
                try:
                    mark = float(input(f"  {sname} ({sid}): "))
                    if 0 <= mark <= 10:
                        marks_dict[cid] = mark
                        break
                    else:
                        print("  Mark must be between 0 and 10!")
                except ValueError:
                    print("  Invalid input! Enter a number.")
        

        students[j] = (sid, sname, students[j][2], marks_dict)
    
    # Main menu loop
    while True:
        print("\n" + "="*40)
        print("1. List all courses")
        print("2. List all students")
        print("3. Show student marks for a course")
        print("4. Exit")
        print("="*40)
        choice = input("Choose an option (1-4): ")
        
        if choice == '1':
            list_courses(courses)
        elif choice == '2':
            list_students(students)
        elif choice == '3':
            show_marks_for_course(courses, students)
        elif choice == '4':
            print("Goodbye! Thanks for using the system.")
            break
        else:
            print("Invalid choice! Try again.")

# Function to list all courses
def list_courses(courses):
    print("\n--- List of Courses ---")
    if not courses:
        print("No courses available.")
        return
    print(f"{'ID':<10} {'Name':<20}")
    print("-" * 30)
    for cid, cname in courses:
        print(f"{cid:<10} {cname:<20}")

# Function to list all students
def list_students(students):
    print("\n--- List of Students ---")
    if not students:
        print("No students registered.")
        return
    print(f"{'ID':<10} {'Name':<20} {'DoB':<12}")
    print("-" * 45)
    for sid, sname, dob, _ in students:
        print(f"{sid:<10} {sname:<20} {dob:<12}")

# Function to show marks for a specific course
def show_marks_for_course(courses, students):
    if not courses:
        print("No courses available!")
        return
    
    print("\nAvailable courses:")
    for i, (cid, cname) in enumerate(courses, 1):
        print(f"  {i}. {cname} ({cid})")
    
    try:
        idx = int(input("Select course by number: ")) - 1
        if 0 <= idx < len(courses):
            selected_cid = courses[idx][0]
            selected_cname = courses[idx][1]
            print(f"\n--- Marks for {selected_cname} ({selected_cid}) ---")
            print(f"{'Student ID':<12} {'Name':<20} {'Mark':<6}")
            print("-" * 40)
            found = False
            for sid, sname, _, marks_dict in students:
                mark = marks_dict.get(selected_cid, "N/A")
                print(f"{sid:<12} {sname:<20} {mark:<6}")
                found = True
            if not found:
                print("No marks entered yet.")
        else:
            print("Invalid course number!")
    except ValueError:
        print("Please enter a valid number!")

if __name__ == "__main__":
    main()