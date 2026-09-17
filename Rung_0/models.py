import csv


class Student:
    scoring_system: dict[int, str] = {
        93: "A",
        90: "A-",
        87: "B+",
        83: "B",
        80: "B-",
        77: "C+",
        73: "C",
        70: "C-",
        60: "D",
        0: "F",
    }

    def __init__(self, student_id: int, name: str, enrollment_year: int):
        self.student_id = student_id
        self.name = name
        self.enrollment_year = enrollment_year
        self.transcript: dict[str, str] = {}

    @property
    def gpa(self) -> float:
        if not self.transcript:
            return 0.0

        points = {
            "A": 4.0,
            "A-": 3.7,
            "B+": 3.3,
            "B": 3.0,
            "B-": 2.7,
            "C+": 2.3,
            "C": 2.0,
            "C-": 1.7,
            "D": 1.0,
            "F": 0.0,
        }

        total_points = sum(
            points[grade] for grade in self.transcript.values()
        )

        return round(total_points / len(self.transcript), 2)

    def get_letter_grade(self, grade: float) -> str:
        if grade > 100 or grade < 0:
            raise ValueError("Grade must be between 0 and 100")

        for minimum in sorted(self.scoring_system, reverse=True):
            if grade >= minimum:
                return self.scoring_system[minimum]

        return "F"

    def add_grade(self, course: str, grade: float):
        self.transcript[course] = self.get_letter_grade(grade)


class GraduateStudent(Student):
    def __init__(
        self,
        student_id: int,
        name: str,
        enrollment_year: int,
        research_topic: str,
        supervisor: str | None = None,
    ):
        super().__init__(student_id, name, enrollment_year)

        self.research_topic = research_topic
        self.supervisor = supervisor

    def assign_supervisor(self, supervisor: str):
        self.supervisor = supervisor


def save_students(students: list[Student], filename: str):
    with open(filename, "w", newline="", encoding="utf-8") as file:
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

        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for student in students:
            # Graduate students have a few extra values to save
            if isinstance(student, GraduateStudent):
                student_type = "graduate"
                research_topic = student.research_topic
                supervisor = student.supervisor or ""
            else:
                student_type = "regular"
                research_topic = ""
                supervisor = ""

            # This gives students without grades an empty CSV row
            if student.transcript:
                transcript_rows = student.transcript.items()
            else:
                transcript_rows = [("", "")]

            # Each course is stored in its own row
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
    students_by_id: dict[int, Student] = {}

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            student_id = int(row["student_id"])

            # Only create the student if they have not been loaded yet
            if student_id not in students_by_id:
                if row["student_type"] == "graduate":
                    student = GraduateStudent(
                        student_id=student_id,
                        name=row["name"],
                        enrollment_year=int(row["enrollment_year"]),
                        research_topic=row["research_topic"],
                        supervisor=row["supervisor"] or None,
                    )
                else:
                    student = Student(
                        student_id=student_id,
                        name=row["name"],
                        enrollment_year=int(row["enrollment_year"]),
                    )

                students_by_id[student_id] = student

            # Empty courses belong to students who have no grades yet
            if row["course"]:
                students_by_id[student_id].transcript[row["course"]] = (
                    row["letter_grade"]
                )

    return list(students_by_id.values())


if __name__ == "__main__":
    fawaz = Student(1001, "Fawaz", 2020)
    fawaz.add_grade("Math", 99)
    fawaz.add_grade("Science", 90)

    ahmed = Student(1002, "Ahmed", 2021)

    sara = GraduateStudent(
        student_id=1003,
        name="Sara",
        enrollment_year=2022,
        research_topic="Machine Learning",
        supervisor="Dr. Abdullah",
    )

    sara.add_grade("Python", 95)
    sara.add_grade("Statistics", 87)

    students = [fawaz, ahmed, sara]

    save_students(students, "students.csv")

    loaded_students = load_students("students.csv")

    for student in loaded_students:
        print()
        print("Student type:", type(student).__name__)
        print("Student ID:", student.student_id)
        print("Name:", student.name)
        print("Enrollment year:", student.enrollment_year)
        print("Transcript:", student.transcript)
        print("GPA:", student.gpa)

        if isinstance(student, GraduateStudent):
            print("Research topic:", student.research_topic)
            print("Supervisor:", student.supervisor)