import json
import csv
from datetime import date, datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
STUDENTS_FILE = DATA_DIR / "students.json"
ATTENDANCE_FILE = DATA_DIR / "attendance.json"
ASSIGNMENTS_FILE = DATA_DIR / "assignments.json"


def load_data(path):
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print(f"Warning: Could not read {path.name}. Starting with empty data.")
        return []


def save_data(path, data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def read_text(prompt, required=True):
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("This field is required.")


def read_number(prompt, minimum=0, maximum=None):
    while True:
        try:
            value = float(input(prompt).strip())
            if value < minimum or (maximum is not None and value > maximum):
                limit = f" and at most {maximum}" if maximum is not None else ""
                print(f"Enter a number of at least {minimum}{limit}.")
                continue
            return value
        except ValueError:
            print("Enter a valid number.")


def pause():
    input("\nPress Enter to continue...")


def find_student(students, student_id):
    return next((student for student in students if student["id"].lower() == student_id.lower()), None)


def select_student(students):
    if not students:
        print("No students found. Add a student first.")
        return None
    student_id = read_text("Student ID: ")
    student = find_student(students, student_id)
    if student is None:
        print("Student not found.")
    return student


def student_management(students):
    while True:
        print("\nSTUDENT MANAGEMENT\n1. Add student\n2. View students\n3. Search student\n4. Update student\n5. Delete student\n0. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            student_id = read_text("Student ID: ")
            if find_student(students, student_id):
                print("A student with this ID already exists.")
                continue
            name = read_text("Name: ")
            course = read_text("Course/class: ")
            students.append({"id": student_id, "name": name, "course": course, "subjects": {}})
            save_data(STUDENTS_FILE, students)
            print("Student added.")
        elif choice == "2":
            if not students:
                print("No students found.")
            for student in students:
                print(f'{student["id"]} | {student["name"]} | {student["course"]}')
        elif choice == "3":
            student = select_student(students)
            if student:
                print(f'\nID: {student["id"]}\nName: {student["name"]}\nCourse: {student["course"]}')
                print("Subjects:", ", ".join(student["subjects"]) or "None")
        elif choice == "4":
            student = select_student(students)
            if student:
                student["name"] = read_text(f'Name [{student["name"]}]: ', required=False) or student["name"]
                student["course"] = read_text(f'Course [{student["course"]}]: ', required=False) or student["course"]
                save_data(STUDENTS_FILE, students)
                print("Student updated.")
        elif choice == "5":
            student = select_student(students)
            if student and input(f'Delete {student["name"]}? (y/N): ').strip().lower() == "y":
                students.remove(student)
                save_data(STUDENTS_FILE, students)
                attendance = [a for a in load_data(ATTENDANCE_FILE) if a["student_id"].lower() != student["id"].lower()]
                assignments = [a for a in load_data(ASSIGNMENTS_FILE) if a["student_id"].lower() != student["id"].lower()]
                save_data(ATTENDANCE_FILE, attendance)
                save_data(ASSIGNMENTS_FILE, assignments)
                print("Student and related records deleted.")
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


def marks_menu(students):
    while True:
        print("\nMARKS & GRADES\n1. Add/update subject marks\n2. View student marks\n0. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            student = select_student(students)
            if not student:
                continue
            subject = read_text("Subject: ")
            maximum = read_number("Maximum marks: ", minimum=0.01)
            marks = read_number("Marks obtained: ", minimum=0, maximum=maximum)
            student["subjects"][subject] = {"marks": marks, "maximum": maximum}
            save_data(STUDENTS_FILE, students)
            print("Marks saved.")
        elif choice == "2":
            student = select_student(students)
            if student:
                if not student["subjects"]:
                    print("No marks recorded.")
                total, maximum = 0, 0
                for subject, record in student["subjects"].items():
                    percent = record["marks"] / record["maximum"] * 100
                    total += record["marks"]
                    maximum += record["maximum"]
                    print(f'{subject}: {record["marks"]:g}/{record["maximum"]:g} ({percent:.2f}%) - {grade(percent)}')
                if maximum:
                    print(f"Overall: {total:g}/{maximum:g} ({total / maximum * 100:.2f}%) - {grade(total / maximum * 100)}")
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


def grade(percent):
    if percent >= 90:
        return "A"
    if percent >= 80:
        return "B"
    if percent >= 70:
        return "C"
    if percent >= 60:
        return "D"
    if percent >= 50:
        return "E"
    return "F"


def attendance_menu(students):
    records = load_data(ATTENDANCE_FILE)
    while True:
        print("\nATTENDANCE\n1. Record attendance\n2. View attendance\n0. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            student = select_student(students)
            if not student:
                continue
            day = read_text(f"Date [{date.today().isoformat()}]: ", required=False) or date.today().isoformat()
            try:
                datetime.strptime(day, "%Y-%m-%d")
            except ValueError:
                print("Use YYYY-MM-DD for the date.")
                continue
            status = read_text("Status (P/A): ").upper()
            if status not in ("P", "A"):
                print("Status must be P or A.")
                continue
            existing = next((r for r in records if r["student_id"].lower() == student["id"].lower() and r["date"] == day), None)
            if existing:
                existing["status"] = status
            else:
                records.append({"student_id": student["id"], "date": day, "status": status})
            save_data(ATTENDANCE_FILE, records)
            print("Attendance saved.")
        elif choice == "2":
            student = select_student(students)
            if student:
                own = [r for r in records if r["student_id"].lower() == student["id"].lower()]
                present = sum(r["status"] == "P" for r in own)
                total = len(own)
                print(f"Present: {present} | Total: {total} | Attendance: {present / total * 100:.2f}%" if total else "No attendance recorded.")
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


def assignment_menu(students):
    records = load_data(ASSIGNMENTS_FILE)
    while True:
        print("\nASSIGNMENTS\n1. Add assignment\n2. View assignments\n3. Mark completed\n0. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            student = select_student(students)
            if not student:
                continue
            title = read_text("Assignment title: ")
            due = read_text("Due date (YYYY-MM-DD): ")
            try:
                datetime.strptime(due, "%Y-%m-%d")
            except ValueError:
                print("Use YYYY-MM-DD for the due date.")
                continue
            records.append({"id": max([a["id"] for a in records], default=0) + 1,
                            "student_id": student["id"], "title": title, "due": due, "completed": False})
            save_data(ASSIGNMENTS_FILE, records)
            print("Assignment added.")
        elif choice == "2":
            if not records:
                print("No assignments found.")
            for item in records:
                status = "Completed" if item["completed"] else "Pending"
                overdue = " | OVERDUE" if not item["completed"] and item["due"] < date.today().isoformat() else ""
                print(f'#{item["id"]} | {item["student_id"]} | {item["title"]} | Due: {item["due"]} | {status}{overdue}')
        elif choice == "3":
            try:
                assignment_id = int(read_text("Assignment number: "))
            except ValueError:
                print("Enter a valid assignment number.")
                continue
            item = next((a for a in records if a["id"] == assignment_id), None)
            if item:
                item["completed"] = True
                save_data(ASSIGNMENTS_FILE, records)
                print("Assignment marked completed.")
            else:
                print("Assignment not found.")
        elif choice == "0":
            return
        else:
            print("Invalid choice.")


def analytics(students):
    if not students:
        print("No student records available.")
        return
    results = []
    for student in students:
        subjects = student["subjects"]
        if subjects:
            marks = sum(s["marks"] for s in subjects.values())
            maximum = sum(s["maximum"] for s in subjects.values())
            results.append((student, marks / maximum * 100))
    if not results:
        print("No marks have been recorded.")
        return
    print(f"Class average: {sum(p for _, p in results) / len(results):.2f}%")
    print("\nStudent performance:")
    for student, percent in sorted(results, key=lambda item: item[1], reverse=True):
        print(f'{student["id"]} | {student["name"]} | {percent:.2f}% | {grade(percent)}')
    print(f'\nTop performer: {max(results, key=lambda item: item[1])[0]["name"]}')


def generate_reports(students):
    student = select_student(students)
    if not student:
        return
    lines = [f'ACADEMIC REPORT: {student["name"]}', f'ID: {student["id"]}', f'Course: {student["course"]}', "", "SUBJECTS"]
    total, maximum = 0, 0
    for name, record in student["subjects"].items():
        percent = record["marks"] / record["maximum"] * 100
        lines.append(f'{name}: {record["marks"]:g}/{record["maximum"]:g} ({percent:.2f}%) Grade {grade(percent)}')
        total += record["marks"]
        maximum += record["maximum"]
    lines.append(f"Overall: {total / maximum * 100:.2f}% Grade {grade(total / maximum * 100)}" if maximum else "Overall: No marks recorded")
    path = DATA_DIR / f'report_{student["id"]}.txt'
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report saved to {path}")


def export_data(students):
    path = DATA_DIR / "student_marks.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Student ID", "Name", "Course", "Subject", "Marks", "Maximum", "Percentage", "Grade"])
        for student in students:
            for subject, record in student["subjects"].items():
                percent = record["marks"] / record["maximum"] * 100
                writer.writerow([student["id"], student["name"], student["course"], subject,
                                 record["marks"], record["maximum"], round(percent, 2), grade(percent)])
    print(f"CSV exported to {path}")


def main():
    students = load_data(STUDENTS_FILE)
    actions = {"1": lambda: student_management(students),
               "2": lambda: marks_menu(students),
               "3": lambda: attendance_menu(students),
               "4": lambda: assignment_menu(students),
               "5": lambda: analytics(students),
               "6": lambda: generate_reports(students),
               "7": lambda: export_data(students)}
    while True:
        print("\n========== GRADEMATE ==========")
        print("1. Student Management\n2. Marks & Grades\n3. Attendance\n4. Assignment Tracker")
        print("5. Academic Analytics\n6. Generate Reports\n7. Export Data\n0. Exit")
        choice = input("===============================\nEnter choice: ").strip()
        if choice == "0":
            print("Thank you for using GradeMate!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Select 0 to 7.")


if __name__ == "__main__":
    main()
