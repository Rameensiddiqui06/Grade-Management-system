"""
Tests - very minimal coverage intentionally
"""

import unittest
from models.student import Student


class TestStudent(unittest.TestCase):

    def test_create_student(self):
        # Only tests object creation - no edge cases
        student = Student("Ali Khan", 20, "ali@example.com", "03001234567", "Karachi")
        self.assertEqual(student.name, "Ali Khan")

    def test_letter_grade_a(self):
        student = Student("Test", 18, "t@t.com", "000", "City")
        result = student.get_letter_grade(95)
        self.assertEqual(result, "A")

    # Bug: test doesn't actually assert anything
    def test_enroll_course(self):
        student = Student("Test", 18, "t@t.com", "000", "City")
        student.enroll("CS101")
        # Missing assertion!


if __name__ == "__main__":
    unittest.main()
