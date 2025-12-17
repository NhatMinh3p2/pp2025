import os
import zlib
import pickle

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

ARCHIVE_PATH = os.path.join(DATA_DIR, "students.dat")

def save_data(students, courses, marks_dict):
    """Write plain text files"""
    # students.txt
    with open(os.path.join(DATA_DIR, "students.txt"), "w", encoding="utf-8") as f:
        for s in students:
            f.write(f"{s.get_id()}|{s.get_name()}|{s.get_dob()}\n")

    # courses.txt
    with open(os.path.join(DATA_DIR, "courses.txt"), "w", encoding="utf-8") as f:
        for c in courses:
            f.write(f"{c.get_id()}|{c.get_name()}|{c.get_credits()}\n")

    # marks.txt
    with open(os.path.join(DATA_DIR, "marks.txt"), "w", encoding="utf-8") as f:
        for course_id, mark_list in marks_dict.items():
            for m in mark_list:
                f.write(f"{m.get_student_id()}|{course_id}|{m.get_mark()}\n")

    # Compress all into students.dat
    data = {
        "students": [(s.get_id(), s.get_name(), s.get_dob()) for s in students],
        "courses": [(c.get_id(), c.get_name(), c.get_credits()) for c in courses],
        "marks": [(m.get_student_id(), m.get_course_id(), m.get_mark()) for cid, mlist in marks_dict.items() for m in mlist]
    }
    compressed = zlib.compress(pickle.dumps(data))
    with open(ARCHIVE_PATH, "wb") as f:
        f.write(compressed)
    print(f"All data saved and compressed to {ARCHIVE_PATH}")

def load_data(StudentCls, CourseCls, MarkCls):
    """Return (students_list, courses_list, marks_dict) if archive exists"""
    if not os.path.exists(ARCHIVE_PATH):
        return None, None, None

    try:
        with open(ARCHIVE_PATH, "rb") as f:
            compressed = f.read()
        data = pickle.loads(zlib.decompress(compressed))

        # Reconstruct Students
        students = [StudentCls(sid, name, dob) for sid, name, dob in data["students"]]

        # Reconstruct Courses
        courses = [CourseCls(sid, name, cred) for sid, name, cred in data["courses"]]
        marks_dict = {c.get_id(): [] for c in courses}

        # Reconstruct Marks
        for sid, cid, mark in data["marks"]:
            m = MarkCls(sid, cid, mark)
            marks_dict[cid].append(m)

        print(f"Data successfully loaded from {ARCHIVE_PATH}")
        return students, courses, marks_dict

    except Exception as e:
        print("Failed to load compressed data:", e)
        return None, None, None