import os
import pickle
import zlib
import threading
import time
from queue import Queue
from domains import Student, Course, Mark

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
ARCHIVE_FILE = os.path.join(DATA_DIR, "students.dat")

# Thread-safe queue for save requests
save_queue = Queue()
save_lock = threading.Lock()
background_thread = None

def _background_saver():
    """Background thread that saves data when requested"""
    print("Background auto-save thread started...")
    while True:
        data_to_save = save_queue.get()
        if data_to_save is None:
            print("Background saver shutting down...")
            break

        students, courses, marks_dict = data_to_save

        try:
            with save_lock:
                payload = {
                    'students': students,
                    'courses': courses,
                    'marks': marks_dict
                }
                compressed = zlib.compress(pickle.dumps(payload, protocol=pickle.HIGHEST_PROTOCOL))
                with open(ARCHIVE_FILE, 'wb') as f:
                    f.write(compressed)
            print(f"Auto-saved successfully ({time.strftime('%H:%M:%S')})")
        except Exception as e:
            print(f"Background save failed: {e}")
        finally:
            save_queue.task_done()

def start_background_saver():
    """Start the background thread (once)"""
    global background_thread
    if background_thread is None or not background_thread.is_alive():
        background_thread = threading.Thread(target=_background_saver, daemon=True)
        background_thread.start()

def save_all_async(students, courses, marks_dict):
    """
    Request a background save — non-blocking!
    """
    save_queue.put((students[:], courses[:], {k: v[:] for k, v in marks_dict.items()}))  # deep-ish copy

def save_all_sync(students, courses, marks_dict):
    """Immediate save — used only on exit"""
    try:
        payload = {
            'students': students,
            'courses': courses,
            'marks': marks_dict
        }
        compressed = zlib.compress(pickle.dumps(payload, protocol=pickle.HIGHEST_PROTOCOL))
        with open(ARCHIVE_FILE, 'wb') as f:
            f.write(compressed)
        print("Final data saved securely.")
    except Exception as e:
        print(f"Final save failed: {e}")

def load_all():
    """Load data on startup"""
    if not os.path.exists(ARCHIVE_FILE):
        print("No saved data found. Starting fresh.")
        return [], [], {}

    try:
        with open(ARCHIVE_FILE, 'rb') as f:
            compressed = f.read()
        data = pickle.loads(zlib.decompress(compressed))

        students = data.get('students', [])
        courses = data.get('courses', [])
        marks_dict = data.get('marks', {})

        print(f"Data loaded: {len(students)} students, {len(courses)} courses")
        return students, courses, marks_dict
    except Exception as e:
        print(f"Failed to load data: {e}. Starting fresh.")
        return [], [], {}

def shutdown_saver():
    """Gracefully stop background thread"""
    save_queue.put(None)
    if background_thread:
        background_thread.join(timeout=3)