# GradeMate

GradeMate is a terminal-based Student Academic Management System developed using Python. It helps manage student records, marks, attendance, assignments, and basic academic performance.

## Features

- Add, view, search, update, and delete student records
- Record and update subject marks
- Calculate percentages and letter grades
- Track student attendance and calculate attendance percentages
- Manage assignments and due dates
- Track pending, completed, and overdue assignments
- View class averages and student performance
- Generate individual academic reports
- Export marks and grades to CSV
- Store data locally using JSON files
- Validate user input and handle common errors

## Technologies Used

- Python 3
- JSON for data storage
- CSV for data export
- `datetime` for dates and deadlines
- `unittest` for basic testing

No external Python packages are required.

## Project Structure

```text
GradeMate/
├── main.py
├── data/
│   └── .gitkeep
├── tests/
│   └── test_academics.py
└── README.md
```

The application creates its JSON data files and generated reports in the `data` directory when needed.

## Main Menu

```text
========== GRADEMATE ==========
1. Student Management
2. Marks & Grades
3. Attendance
4. Assignment Tracker
5. Academic Analytics
6. Generate Reports
7. Export Data
0. Exit
===============================
Enter choice:
```

## Features in Detail

### Student Management

- Add students with a unique ID, name, and course or class
- View all student records
- Search for a student by ID
- Update student details
- Delete student records and their associated attendance and assignment records

### Marks and Grades

- Add or update marks for each subject
- Calculate subject-wise percentages
- Calculate overall percentage using total marks obtained divided by total maximum marks
- Assign grades using the following scale

| Percentage | Grade |
|---:|:---|
| 90–100 | A |
| 80–89.99 | B |
| 70–79.99 | C |
| 60–69.99 | D |
| 50–59.99 | E |
| Below 50 | F |

### Attendance

- Record attendance as present (`P`) or absent (`A`)
- Store attendance by student and date
- Update an existing attendance entry for the same student and date
- Calculate attendance percentage

Attendance percentage is calculated as:

```text
(Present sessions / Total recorded sessions) * 100
```

### Assignment Tracker

- Add assignments with a title and due date
- View assignment status
- Mark assignments as completed
- Identify pending and overdue assignments

Dates must use the `YYYY-MM-DD` format.

### Academic Analytics

- Calculate the average percentage of students with recorded marks
- Display student performance in descending order
- Identify the top-performing student among students with recorded marks

### Reports and Export

- Generate a text report for an individual student
- Export recorded subject marks and grades to a CSV file
- Open the CSV file using spreadsheet software such as Microsoft Excel or Google Sheets

## Requirements

- Python 3.9 or later
- A terminal or command prompt

No third-party dependencies are needed.

## Installation and Usage

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Open the project directory:

```bash
cd GradeMate
```

Run the application:

```bash
python main.py
```

On some systems, use `python3` instead:

```bash
python3 main.py
```

Follow the menu prompts to use the application.

## Running Tests

Run the included unit tests from the project directory:

```bash
python -m unittest discover -s tests
```

## Data Storage

GradeMate stores information locally in JSON files under `data/`:

- `students.json` — student details and subject marks
- `attendance.json` — attendance entries
- `assignments.json` — assignment details and completion status

Generated text reports and CSV exports are also saved in this directory. Keep a backup of the `data` directory if the records need to be preserved.

## Learning Objectives

This project demonstrates the use of:

- Variables and data types
- Conditional statements and loops
- Functions
- Lists and dictionaries
- File handling
- JSON and CSV processing
- Exception handling
- Date and time handling
- Modular programming
- Basic unit testing

## Scope and Future Enhancements

The current version is designed as a lightweight command-line application with local file storage. Possible future enhancements include a graphical interface, SQLite storage, PDF reports, configurable grading scales, and additional analytics.
