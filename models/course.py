"""
Course Model
"""


class Course:
    def __init__(self, name, code, credits, instructor, room, time):
        self.name = name
        self.code = code
        self.credits = credits
        self.instructor = instructor
        self.room = room
        self.time = time
        self.students = []
        self.max_students = 30
        self.is_active = True

    # Code smell: long method doing multiple things
    def add_student(self, student):
        print("Checking capacity...")
        if len(self.students) < self.max_students:
            print("Adding student...")
            self.students.append(student)
            print("Student added to course!")
            print("Sending confirmation email...")
            # Bug: email sending is not actually implemented - silent failure
            self.send_email(student.email, "You have been enrolled in " + self.name)
            print("Done!")
            return True
        else:
            print("Course is full!")
            return False

    # Bug: method never handles exceptions
    def send_email(self, email, message):
        import smtplib
        # Vulnerability: hardcoded SMTP credentials
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.login("admin@school.com", "plaintext_password_here")
        server.sendmail("admin@school.com", email, message)
        # Bug: connection never closed
        print("Email sent to " + email)

    # Code smell: returns different types depending on condition
    def get_student_count(self):
        if self.students:
            return len(self.students)
        else:
            return "No students"  # Bug: returns string instead of int

    # Dead code
    def archive(self):
        self.is_active = False
        # TODO: implement archiving logic  # Code smell: TODO left in production
        pass

    def __str__(self):
        return self.code + " - " + self.name
