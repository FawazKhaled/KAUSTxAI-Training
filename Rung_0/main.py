from pathlib import Path

from manager import StudentManager
from models import GraduateStudent, Student
from storage import load_students, save_students


# Using the location of this file makes the data path work
# even when the program is started from another folder.
PROJECT_FOLDER = Path(__file__).resolve().parent
DATA_FOLDER = PROJECT_FOLDER / "Data"
DATA_FILE = DATA_FOLDER / "students.csv"


def read_integer(message: str) -> int:
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Please enter a whole number.")


def read_float(message: str) -> float:
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Please enter a valid number.")


def display_student(student: Student) -> None:
    print()
    print(student)

    if student.transcript:
        print("Transcript:")

        for course, grade in student.transcript.items():
            print(f"  {course}: {grade}")
    else:
        print("Transcript: No grades recorded")


def display_students(students: list[Student]) -> None:
    if not students:
        print("\nNo matching students were found.")
        return

    for student in students:
        display_student(student)


def add_regular_student(manager: StudentManager) -> None:
    print("\nAdd Regular Student")

    student_id = read_integer("Student ID: ")
    name = input("Name: ")
    enrollment_year = read_integer("Enrollment year: ")

    try:
        student = Student(
            student_id=student_id,
            name=name,
            enrollment_year=enrollment_year,
        )

        manager.add_student(student)
        print("Student added successfully.")

    except ValueError as error:
        print(f"Could not add student: {error}")


def add_graduate_student(manager: StudentManager) -> None:
    print("\nAdd Graduate Student")

    student_id = read_integer("Student ID: ")
    name = input("Name: ")
    enrollment_year = read_integer("Enrollment year: ")
    research_topic = input("Research topic: ")
    supervisor = input(
        "Supervisor name, or press Enter if none is assigned: "
    )

    try:
        student = GraduateStudent(
            student_id=student_id,
            name=name,
            enrollment_year=enrollment_year,
            research_topic=research_topic,
            supervisor=supervisor or None,
        )

        manager.add_student(student)
        print("Graduate student added successfully.")

    except ValueError as error:
        print(f"Could not add graduate student: {error}")


def find_student(manager: StudentManager) -> None:
    print("\nFind Student")

    print("1. Search by student ID")
    print("2. Search by name")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        student_id = read_integer("Student ID: ")
        student = manager.find_student(student_id)

        if student is None:
            print("Student not found.")
        else:
            display_student(student)

    elif choice == "2":
        name = input("Enter all or part of the name: ")
        matches = manager.find_by_name(name)
        display_students(matches)

    else:
        print("Invalid option.")


def add_grade(manager: StudentManager) -> None:
    print("\nAdd or Update Grade")

    student_id = read_integer("Student ID: ")
    course = input("Course name: ")
    score = read_float("Numerical score: ")

    try:
        manager.add_grade(student_id, course, score)
        print("Grade saved successfully.")

    except (KeyError, ValueError) as error:
        print(f"Could not save grade: {error}")


def remove_grade(manager: StudentManager) -> None:
    print("\nRemove Grade")

    student_id = read_integer("Student ID: ")
    course = input("Course name: ")

    try:
        manager.remove_grade(student_id, course)
        print("Grade removed successfully.")

    except KeyError as error:
        print(f"Could not remove grade: {error}")


def filter_students(manager: StudentManager) -> None:
    print("\nFilter Students")
    print("1. Filter by enrollment year")
    print("2. Filter by minimum GPA")
    print("3. Show graduate students")

    choice = input("Choose an option: ").strip()

    try:
        if choice == "1":
            year = read_integer("Enrollment year: ")
            matches = manager.filter_by_enrollment_year(year)
            display_students(matches)

        elif choice == "2":
            minimum_gpa = read_float("Minimum GPA: ")
            matches = manager.filter_by_minimum_gpa(minimum_gpa)
            display_students(matches)

        elif choice == "3":
            matches = manager.get_graduate_students()
            display_students(matches)

        else:
            print("Invalid option.")

    except ValueError as error:
        print(f"Could not filter students: {error}")


def remove_student(manager: StudentManager) -> None:
    print("\nRemove Student")

    student_id = read_integer("Student ID: ")
    student = manager.find_student(student_id)

    if student is None:
        print("Student not found.")
        return

    display_student(student)

    confirmation = input(
        "\nType yes to permanently remove this student: "
    ).strip().lower()

    if confirmation != "yes":
        print("Removal cancelled.")
        return

    manager.remove_student(student_id)
    print("Student removed successfully.")


def save_records(manager: StudentManager) -> None:
    try:
        DATA_FOLDER.mkdir(exist_ok=True)

        save_students(
            manager.get_all_students(),
            str(DATA_FILE),
        )

        print(f"Records saved to {DATA_FILE.name}.")

    except OSError as error:
        print(f"Could not save records: {error}")


def show_menu() -> None:
    print("\nStudent Records Manager")
    print("1. Add regular student")
    print("2. Add graduate student")
    print("3. Find student")
    print("4. List all students")
    print("5. Add or update grade")
    print("6. Remove grade")
    print("7. Filter students")
    print("8. Remove student")
    print("9. Save records")
    print("0. Save and exit")


def main() -> None:
    DATA_FOLDER.mkdir(exist_ok=True)

    try:
        loaded_students = load_students(str(DATA_FILE))
        manager = StudentManager(loaded_students)
    except (OSError, ValueError, KeyError) as error:
        print(f"Could not load existing records: {error}")
        print("The program will start with an empty student list.")
        manager = StudentManager()

    print(
        f"Loaded {manager.student_count()} student record(s)."
    )

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_regular_student(manager)

        elif choice == "2":
            add_graduate_student(manager)

        elif choice == "3":
            find_student(manager)

        elif choice == "4":
            display_students(manager.get_all_students())

        elif choice == "5":
            add_grade(manager)

        elif choice == "6":
            remove_grade(manager)

        elif choice == "7":
            filter_students(manager)

        elif choice == "8":
            remove_student(manager)

        elif choice == "9":
            save_records(manager)

        elif choice == "0":
            save_records(manager)
            print("Goodbye.")
            break

        else:
            print("Invalid option. Choose a number from the menu.")


if __name__ == "__main__":
    main()