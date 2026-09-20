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

    grade_points: dict[str, float] = {
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

    def __init__(
        self,
        student_id: int,
        name: str,
        enrollment_year: int,
    ):
        if student_id <= 0:
            raise ValueError("Student ID must be positive")

        if not name.strip():
            raise ValueError("Student name cannot be empty")

        if enrollment_year <= 0:
            raise ValueError("Enrollment year must be positive")

        self.student_id = student_id
        self.name = name.strip()
        self.enrollment_year = enrollment_year
        self.transcript: dict[str, str] = {}

    @property
    def gpa(self) -> float:
        if not self.transcript:
            return 0.0

        total_points = sum(
            self.grade_points[grade]
            for grade in self.transcript.values()
        )

        return round(total_points / len(self.transcript), 2)

    def get_letter_grade(self, score: float) -> str:
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100")

        for minimum_score in sorted(
            self.scoring_system,
            reverse=True,
        ):
            if score >= minimum_score:
                return self.scoring_system[minimum_score]

        return "F"

    def add_grade(self, course: str, score: float) -> None:
        course = course.strip()

        if not course:
            raise ValueError("Course name cannot be empty")

        self.transcript[course] = self.get_letter_grade(score)

    def remove_grade(self, course: str) -> None:
        if course not in self.transcript:
            raise KeyError(f"No grade found for {course}")

        del self.transcript[course]

    def get_grade(self, course: str) -> str | None:
        return self.transcript.get(course)

    def __str__(self) -> str:
        return (
            f"{self.student_id}: {self.name} "
            f"({self.enrollment_year}), GPA: {self.gpa:.2f}"
        )


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

        if not research_topic.strip():
            raise ValueError("Research topic cannot be empty")

        self.research_topic = research_topic.strip()
        self.supervisor = supervisor.strip() if supervisor else None

    def assign_supervisor(self, supervisor: str) -> None:
        supervisor = supervisor.strip()

        if not supervisor:
            raise ValueError("Supervisor name cannot be empty")

        self.supervisor = supervisor

    def __str__(self) -> str:
        supervisor = self.supervisor or "Not assigned"

        return (
            f"{super().__str__()}, "
            f"Research: {self.research_topic}, "
            f"Supervisor: {supervisor}"
        )