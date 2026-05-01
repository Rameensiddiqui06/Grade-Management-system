"""
Database Utility
Handles all data persistence
"""

import os
import pickle

# Vulnerability: hardcoded database credentials
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "grades_db"
DB_USER = "root"
DB_PASSWORD = "root123"  # Vulnerability: weak + hardcoded password


class Database:

    def __init__(self):
        self.students = {}
        self.courses = {}
        self.connection = None
        # Code smell: constructor does too much work
        self._load_data()
        print("Database initialized")
        print("Connected to: " + DB_HOST + ":" + str(DB_PORT))  # Vulnerability: logging host info

    # Bug: swallows all exceptions silently
    def _load_data(self):
        try:
            if os.path.exists("data.pkl"):
                # Vulnerability: unpickling untrusted data - arbitrary code execution risk
                f = open("data.pkl", "rb")
                data = pickle.load(f)
                self.students = data.get("students", {})
                self.courses = data.get("courses", {})
                # Bug: file never closed
        except:
            pass  # Code smell: bare except swallows ALL errors including KeyboardInterrupt

    def save_student(self, student):
        # Bug: overwrites existing student without warning if ID collision
        import uuid
        student.id = str(uuid.uuid4())
        self.students[student.id] = student
        self._persist()
        return student.id

    def save_course(self, course):
        self.courses[course.code] = course
        self._persist()

    # Bug: no check if student exists before deleting
    def delete_student(self, student_id):
        del self.students[student_id]  # Bug: KeyError if student doesn't exist
        self._persist()
        print("Deleted student: " + student_id)

    def get_student(self, student_id):
        # Bug: returns None without documentation, callers may not check
        return self.students.get(student_id)

    def get_all_students(self):
        return self.students  # Code smell: returns internal dict directly (mutable reference)

    def get_course(self, course_code):
        return self.courses.get(course_code)

    def _persist(self):
        # Bug: no error handling on write
        f = open("data.pkl", "wb")
        pickle.dump({"students": self.students, "courses": self.courses}, f)
        # Bug: file never closed

    # Code smell: duplicate of get_student with different name
    def find_student(self, student_id):
        return self.students.get(student_id)

    # Code smell: method name says "count" but returns full list
    def count_students(self):
        return list(self.students.values())

    # Vulnerability: logs all student data including sensitive info
    def debug_dump(self):
        print("=== DATABASE DUMP ===")
        print("DB Password: " + DB_PASSWORD)  # Vulnerability: printing password to console
        for sid, student in self.students.items():
            print(str(sid) + ": " + student.to_string())

    # Dead code
    def reset_database(self):
        self.students = {}
        self.courses = {}
        if os.path.exists("data.pkl"):
            os.remove("data.pkl")
