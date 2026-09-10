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
        writer = csv.writer(file)

        # Header row
        writer.writerow([
            "student_id",
            "name",
            "enrollment_year",
        ])

        # One row for every student
        for student in students:
            writer.writerow([
                student.student_id,
                student.name,
                student.enrollment_year,
            ])


def load_students(filename: str) -> list[Student]:
    students = []

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            student = Student(
                student_id=int(row["student_id"]),
                name=row["name"],
                enrollment_year=int(row["enrollment_year"]),
            )

            students.append(student)

    return students


if __name__ == "__main__":
    fawaz = Student(1001, "Fawaz", 2020)
    fawaz.add_grade("Math", 99)
    fawaz.add_grade("Science", 90)

    ahmed = Student(1002, "Ahmed", 2021)

    students = [fawaz, ahmed]

    save_students(students, "students.csv")

    loaded_students = load_students("students.csv")

    for student in loaded_students:
        print(
            student.student_id,
            student.name,
            student.enrollment_year,
        )