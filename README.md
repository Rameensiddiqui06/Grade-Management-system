# Student Grade Management System

A Python-based CLI application for managing student grades, courses, and generating reports.

## Project Structure

```
grade-management-system/
├── main.py                  # Entry point
├── models/
│   ├── student.py           # Student data model
│   └── course.py            # Course data model
├── services/
│   ├── grade_service.py     # Grade assignment and statistics
│   └── report_service.py    # Report generation
├── utils/
│   ├── database.py          # Data persistence layer
│   └── helpers.py           # Utility functions
└── tests/
    └── test_student.py      # Unit tests
```

## Features

- Add and manage students
- Create and manage courses
- Assign grades to students
- Generate student reports
- Calculate GPA and statistics

## Requirements

- Python 3.8+

## How to Run

```bash
python main.py
```

## Running Tests

```bash
python -m unittest discover tests/
```
