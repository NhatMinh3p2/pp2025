import os
import pickle
import zlib
from domains import Student, Course, Mark

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
ARCHIVE_FILE = os.path.join(DATA_DIR, "students.dat")

def save_all(students, courses, marks_dict):
    """
    Save everything in ONE compressed pickle file
    """
    data = {
        'students': students,           
        'courses': courses,
        'marks': marks_dict             
    }
    try:
        compressed = zlib.compress(pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL))
        with open(ARCHIVE_FILE, 'wb') as f:
            f.write(compressed)
        print(f"✓ All data saved & compressed → {ARCHIVE_FILE}")
    except Exception as e:
        print(f"✗ Save failed: {e}")

def load_all():
    """
    Load and return (students, courses, marks_dict)
    If no file → return empty
    """
    if not os.path.exists(ARCHIVE_FILE):
        print("No saved data found. Starting fresh.")
        return [], [], {}

    try:
        with open(ARCHIVE_FILE, 'rb') as f:
            compressed_data = f.read()
        data = pickle.loads(zlib.decompress(compressed_data))

        students = data.get('students', [])
        courses = data.get('courses', [])
        marks_dict = data.get('marks', {})

        print(f"✓ Data loaded successfully from {ARCHIVE_FILE}")
        print(f"   → {len(students)} students, {len(courses)} courses, marks recorded.")
        return students, courses, marks_dict

    except Exception as e:
        print(f"✗ Failed to load data: {e}")
        print("Starting with empty system...")
        return [], [], {}