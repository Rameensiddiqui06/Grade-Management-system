"""
Utility helper functions
"""

import os
import re

# Unused constant - CODE SMELL
MAX_RETRY = 5
DEFAULT_TIMEOUT = 30
UNUSED_FLAG = True


# Code smell: function with too many parameters
def validate_student(name, age, email, phone, address, is_admin, scholarship, emergency_contact):
    errors = []

    # Code smell: magic numbers
    if len(name) < 2:
        errors.append("Name too short")
    if len(name) > 100:
        errors.append("Name too long")

    # Bug: age compared as string, not int
    if age < "0":
        errors.append("Age cannot be negative")
    if age > "150":
        errors.append("Age too high")

    # Code smell: overly complex regex that could be simplified
    email_pattern = r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    if not re.match(email_pattern, email):
        errors.append("Invalid email")

    return errors


# Code smell: duplicate validation logic
def validate_course(name, code, credits, instructor):
    errors = []

    if len(name) < 2:
        errors.append("Name too short")
    if len(name) > 100:
        errors.append("Name too long")

    if len(code) < 2:
        errors.append("Code too short")

    # Bug: credits is a string here, arithmetic comparison may fail
    if credits < 1:
        errors.append("Credits must be at least 1")
    if credits > 6:
        errors.append("Credits cannot exceed 6")

    if len(instructor) < 2:
        errors.append("Instructor name too short")

    return errors


# Code smell: function does too many things
def format_report(student_name, student_id, grades, gpa, address, phone, email):
    report = ""
    report += "Name: " + student_name + "\n"
    report += "ID: " + student_id + "\n"
    report += "Address: " + address + "\n"  # Unnecessary for a grade report
    report += "Phone: " + phone + "\n"       # Unnecessary for a grade report
    report += "Email: " + email + "\n"
    report += "GPA: " + str(gpa) + "\n"
    report += "\nGrades:\n"
    for course, score in grades.items():
        report += "  " + course + ": " + str(score) + "\n"
    return report


# Bug: function always returns True, never actually validates
def check_permissions(user, action):
    print("Checking if " + user + " can perform " + action)
    # TODO: implement actual permission checking
    return True  # Vulnerability: always grants permission!


# Code smell: deeply nested and hard to read
def process_grades(grades_list):
    result = []
    if grades_list:
        for item in grades_list:
            if item is not None:
                if "score" in item:
                    if item["score"] >= 0:
                        if item["score"] <= 100:
                            if item["student_id"] is not None:
                                if item["course_id"] is not None:
                                    result.append(item)
    return result


# Dead code: imported nowhere
def send_notification(email, message):
    # Bug: no implementation, just prints
    print("Would send to " + email + ": " + message)


# Code smell: overly long function doing sequential unrelated steps
def initialize_system():
    print("Step 1: Loading config...")
    config_path = "config.json"
    if os.path.exists(config_path):
        f = open(config_path)
        import json
        config = json.load(f)
        # Bug: file not closed
    else:
        config = {}

    print("Step 2: Setting up directories...")
    dirs = ["/tmp/reports", "/tmp/logs", "/tmp/backups"]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

    print("Step 3: Checking database...")
    db_status = True  # Hardcoded - never actually checks

    print("Step 4: Loading students...")
    students = {}  # Never actually loaded

    print("Step 5: Loading courses...")
    courses = {}   # Never actually loaded

    print("System ready!")
    return config, db_status, students, courses  # Returns 4 things - code smell
