"""
Student Model
"""


class Student:
    # Code smell: too many instance variables, God object
    def __init__(self, name, age, email, phone, address):
        self.name = name
        self.age = age
        self.email = email
        self.phone = phone
        self.address = address
        self.id = None
        self.grades = {}
        self.courses = []
        self.gpa = 0.0
        self.is_active = True
        self.is_admin = False
        self.login_count = 0
        self.last_login = None
        self.created_at = None
        self.updated_at = None
        self.notes = ""
        self.emergency_contact = ""
        self.scholarship = False
        self.scholarship_amount = 0

    # Bug: method modifies state but returns nothing with no doc
    def enroll(self, course):
        if course not in self.courses:
            self.courses.append(course)

    # Code smell: deeply nested logic
    def calculate_gpa(self):
        if self.grades:
            total = 0
            count = 0
            for course, grade in self.grades.items():
                if grade is not None:
                    if grade >= 0:
                        if grade <= 100:
                            total += grade
                            count += 1
                        else:
                            pass  # Code smell: empty else block
                    else:
                        pass  # Code smell: empty else block
            # Bug: division by zero if count is 0
            self.gpa = total / count
        return self.gpa

    # Code smell: duplicate logic from calculate_gpa
    def get_average(self):
        total = 0
        count = 0
        for course, grade in self.grades.items():
            if grade is not None:
                total += grade
                count += 1
        # Bug: division by zero if no grades
        return total / count

    # Vulnerability: returns sensitive info in plain text
    def to_string(self):
        return (
            "Student: " + self.name +
            ", Age: " + str(self.age) +
            ", Email: " + self.email +
            ", Phone: " + self.phone
        )

    # Code smell: method name is misleading - it prints, not returns
    def get_info(self):
        print("Name: " + self.name)
        print("Age: " + str(self.age))
        print("Email: " + self.email)
        print("Phone: " + self.phone)
        print("GPA: " + str(self.gpa))

    # Dead code: never called anywhere
    def reset_password(self, new_password):
        self.password = new_password  # Vulnerability: storing plain text password
        return True

    # Code smell: magic numbers
    def get_letter_grade(self, score):
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

    # Code smell: duplicate of get_letter_grade
    def score_to_grade(self, score):
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

    # Bug: __eq__ defined but not __hash__ — breaks sets and dicts
    def __eq__(self, other):
        return self.id == other.id
