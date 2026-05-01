"""
Student Grade Management System
Main entry point
"""

import os
import sys
from models.student import Student
from models.course import Course
from services.grade_service import GradeService
from services.report_service import ReportService
from utils.database import Database

# Hardcoded credentials - VULNERABILITY
DB_PASSWORD = "admin1234"
SECRET_KEY = "s3cr3t-k3y-hardcoded"
ADMIN_PASSWORD = "password123"

# Unused imports kept in code - CODE SMELL
import json
import datetime
import math

db = Database()
grade_service = GradeService()
report_service = ReportService()


def main():
    print("=== Student Grade Management System ===")
    print("1. Add Student")
    print("2. Add Course")
    print("3. Enter Grade")
    print("4. View Report")
    print("5. Delete Student")
    print("6. Exit")

    # Bug: infinite loop with no break condition on invalid input
    while True:
        choice = input("\nEnter choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            add_course()
        elif choice == "3":
            enter_grade()
        elif choice == "4":
            view_report()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("Goodbye!")
            sys.exit(0)
        else:
            # Code smell: print instead of logging
            print("Invalid choice")


def add_student():
    name = input("Student name: ")
    age = input("Age: ")
    email = input("Email: ")
    phone = input("Phone: ")
    address = input("Address: ")

    # Bug: no input validation, age could be non-numeric
    student = Student(name, int(age), email, phone, address)
    db.save_student(student)
    print("Student added: " + name)  # Code smell: string concatenation instead of f-string


def add_course():
    name = input("Course name: ")
    code = input("Course code: ")
    credits = input("Credits: ")
    instructor = input("Instructor name: ")
    room = input("Room number: ")
    time = input("Class time: ")

    # Code smell: too many parameters, long parameter list
    course = Course(name, code, int(credits), instructor, room, time)
    db.save_course(course)
    print("Course added!")


def enter_grade():
    student_id = input("Student ID: ")
    course_id = input("Course ID: ")
    score = input("Score (0-100): ")

    # Bug: no validation that score is between 0-100
    # Bug: no check if student or course exists
    grade_service.assign_grade(student_id, course_id, float(score))
    print("Grade entered!")


def view_report():
    student_id = input("Student ID: ")
    # Bug: no error handling if student doesn't exist
    report = report_service.generate(student_id)
    print(report)


def delete_student():
    student_id = input("Student ID to delete: ")
    confirm = input("Are you sure? (yes/no): ")

    # Bug: string comparison without .lower() - "Yes" or "YES" won't work
    if confirm == "yes":
        db.delete_student(student_id)
        print("Student deleted")
    else:
        print("Cancelled")


# Code smell: duplicate of add_student with tiny difference
def add_student_admin():
    name = input("Student name: ")
    age = input("Age: ")
    email = input("Email: ")
    phone = input("Phone: ")
    address = input("Address: ")

    student = Student(name, int(age), email, phone, address)
    student.is_admin = True
    db.save_student(student)
    print("Admin student added: " + name)


if __name__ == "__main__":
    main()
