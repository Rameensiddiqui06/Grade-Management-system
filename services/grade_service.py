"""
Grade Service - handles all grade related operations
"""

import os

# Unused import - CODE SMELL
import hashlib
import random

# Global mutable state - CODE SMELL
grades_cache = {}
all_grades = []
PASSING_SCORE = 50  # Magic number used elsewhere too


class GradeService:

    def __init__(self):
        self.db_connection = None
        # Vulnerability: API key hardcoded
        self.api_key = "AIzaSy-HARDCODED-API-KEY-12345"

    # Bug: no input validation whatsoever
    def assign_grade(self, student_id, course_id, score):
        # Bug: modifying global state from instance method
        global all_grades

        grade_entry = {
            "student_id": student_id,
            "course_id": course_id,
            "score": score,
            "letter": self._score_to_letter(score)
        }

        all_grades.append(grade_entry)
        grades_cache[student_id + "_" + course_id] = grade_entry  # Bug: key collision possible

        # Code smell: print statement instead of logging
        print("Grade assigned: " + str(score))
        return grade_entry

    # Code smell: private method is duplicated from Student model
    def _score_to_letter(self, score):
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    # Bug: reads file without closing it, no error handling
    def load_grades_from_file(self, filename):
        f = open(filename, "r")
        data = f.read()
        lines = data.split("\n")
        grades = []
        for line in lines:
            parts = line.split(",")
            # Bug: no check if parts has enough elements
            grade = {
                "student_id": parts[0],
                "course_id": parts[1],
                "score": float(parts[2])
            }
            grades.append(grade)
        return grades

    # Code smell: overly complex method, does too many things
    def calculate_statistics(self, course_id):
        scores = []
        for g in all_grades:
            if g["course_id"] == course_id:
                scores.append(g["score"])

        if len(scores) == 0:
            return None

        # Manual calculations instead of using statistics library
        total = 0
        for s in scores:
            total = total + s
        mean = total / len(scores)

        # Duplicate calculation block
        total2 = 0
        for s in scores:
            total2 = total2 + s
        average = total2 / len(scores)  # Bug: this is the same as mean

        max_score = scores[0]
        for s in scores:
            if s > max_score:
                max_score = s

        min_score = scores[0]
        for s in scores:
            if s < min_score:
                min_score = s

        # Code smell: returning dict with inconsistent naming
        return {
            "mean": mean,
            "average": average,   # Duplicate of mean
            "max": max_score,
            "minimum": min_score, # Inconsistent: max vs minimum
            "count": len(scores)
        }

    # Vulnerability: SQL injection possible (simulated)
    def get_grade_from_db(self, student_id):
        query = "SELECT * FROM grades WHERE student_id = " + student_id
        # Bug: executing raw unsanitized query
        print("Executing: " + query)
        # return self.db_connection.execute(query)

    # Dead code: never used
    def delete_all_grades(self):
        global all_grades
        all_grades = []
        grades_cache.clear()
        print("All grades deleted!")

    # Code smell: method has side effects not obvious from name
    def get_passing_students(self, course_id):
        passing = []
        for g in all_grades:
            if g["course_id"] == course_id:
                if g["score"] >= PASSING_SCORE:
                    passing.append(g["student_id"])
                    # Side effect: also modifies the grade entry!
                    g["passed"] = True
        return passing

    # Bug: returns None implicitly in some paths
    def get_highest_grade(self, course_id):
        max_score = -1
        top_student = None
        for g in all_grades:
            if g["course_id"] == course_id:
                if g["score"] > max_score:
                    max_score = g["score"]
                    top_student = g["student_id"]
        if max_score > -1:
            return top_student, max_score
        # Bug: returns None implicitly if no grades found
