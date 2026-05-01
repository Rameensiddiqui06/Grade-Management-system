"""
Report Service - generates student and course reports
"""

# Unused imports
import os
import sys
import json

from services.grade_service import GradeService, all_grades, PASSING_SCORE

grade_service = GradeService()


class ReportService:

    def __init__(self):
        # Code smell: magic string
        self.report_format = "text"
        self.output_path = "/tmp/reports"   # Hardcoded path

    # Bug: no error handling, no validation
    def generate(self, student_id):
        student_grades = []
        for g in all_grades:
            if g["student_id"] == student_id:
                student_grades.append(g)

        # Bug: crashes if student has no grades (division by zero)
        total = sum(g["score"] for g in student_grades)
        average = total / len(student_grades)

        report = "=== STUDENT REPORT ===\n"
        report = report + "Student ID: " + student_id + "\n"
        report = report + "Total Courses: " + str(len(student_grades)) + "\n"
        report = report + "Average Score: " + str(average) + "\n"

        # Code smell: duplicate of _score_to_letter in GradeService
        if average >= 90:
            letter = "A"
        elif average >= 80:
            letter = "B"
        elif average >= 70:
            letter = "C"
        elif average >= 60:
            letter = "D"
        else:
            letter = "F"

        report = report + "Overall Grade: " + letter + "\n"

        # Code smell: inconsistent return - sometimes returns, sometimes prints
        if self.report_format == "print":
            print(report)
        else:
            return report

    # Code smell: almost identical to generate(), just with different header
    def generate_admin_report(self, student_id):
        student_grades = []
        for g in all_grades:
            if g["student_id"] == student_id:
                student_grades.append(g)

        total = sum(g["score"] for g in student_grades)
        # Bug: division by zero again
        average = total / len(student_grades)

        report = "=== ADMIN STUDENT REPORT ===\n"
        report = report + "Student ID: " + student_id + "\n"
        report = report + "Total Courses: " + str(len(student_grades)) + "\n"
        report = report + "Average Score: " + str(average) + "\n"

        return report

    # Bug: writes to file without checking if directory exists
    def save_report_to_file(self, student_id):
        report = self.generate(student_id)
        filename = self.output_path + "/" + student_id + "_report.txt"
        # Bug: file opened but never closed
        f = open(filename, "w")
        f.write(report)
        print("Report saved to " + filename)

    # Vulnerability: student_id used directly in filename - path traversal risk
    def get_saved_report(self, student_id):
        filename = self.output_path + "/" + student_id + "_report.txt"
        # Bug: no error handling if file doesn't exist
        f = open(filename, "r")
        return f.read()

    # Dead code: never called
    def clear_all_reports(self):
        import shutil
        shutil.rmtree(self.output_path)
        os.makedirs(self.output_path)

    # Code smell: method does nothing useful, just wraps another call
    def refresh(self, student_id):
        return self.generate(student_id)
