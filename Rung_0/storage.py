import csv
import os

from models import GraduateStudent, Student


def save_students(students: list[Student], filename: str) -> None:
    columns = [
        "student_type",
        "student_id",
        "name",
        "enrollment_year",
        "research_topic",
        "supervisor",
        "course",
        "letter_grade",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for student in students:
            if isinstance(student, GraduateStudent):
                student_type = "graduate"
                research_topic = student.research_topic
                supervisor = student.supervisor or ""
            else:
                student_type = "regular"
                research_topic = ""
                supervisor = ""

            # Each course gets its own row in the CSV file.
            # A student without grades still needs one empty row.
            if student.transcript:
                transcript_rows = student.transcript.items()
            else:
                transcript_rows = [("", "")]

            for course, letter_grade in transcript_rows:
                writer.writerow({
                    "student_type": student_type,
                    "student_id": student.student_id,
                    "name": student.name,
                    "enrollment_year": student.enrollment_year,
                    "research_topic": research_topic,
                    "supervisor": supervisor,
                    "course": course,
                    "letter_grade": letter_grade,
                })


def load_students(filename: str) -> list[Student]:
    # The program starts with no records if the file does not exist yet.
    if not os.path.exists(filename):
        return []

    students_by_id: dict[int, Student] = {}

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            student_id = int(row["student_id"])

            # A student may appear in several rows because each course
            # is stored separately. Create the object only once.
            if student_id not in students_by_id:
                if row["student_type"] == "graduate":
                    student = GraduateStudent(
                        student_id=student_id,
                        name=row["name"],
                        enrollment_year=int(row["enrollment_year"]),
                        research_topic=row["research_topic"],
                        supervisor=row["supervisor"] or None,
                    )
                elif row["student_type"] == "regular":
                    student = Student(
                        student_id=student_id,
                        name=row["name"],
                        enrollment_year=int(row["enrollment_year"]),
                    )
                else:
                    raise ValueError(
                        f"Unknown student type: {row['student_type']}"
                    )

                students_by_id[student_id] = student

            if row["course"]:
                students_by_id[student_id].transcript[row["course"]] = (
                    row["letter_grade"]
                )

    return list(students_by_id.values())