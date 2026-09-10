class Student:
    scoring_system: dict[int, str] = {93: "A",
        90: "A-",
        87: "B+",
        83: "B",
        80: "B-",
        77: "C+",
        73: "C",
        70: "C-",
        60: "D",
        0: "F"}

    @property
    def gpa(self) -> float:
        if not self.Transcript:
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
        return round(sum(points[grade] for grade in self.Transcript.values()) / len(self.Transcript), 2)

    def get_letter_grade(self, grade: float) -> str:
        for minimum in sorted(self.scoring_system, reverse=True):
            if grade > 100 or grade < 0:
                raise ValueError("Invalid grade")
            elif grade >= minimum:
                return self.scoring_system[minimum]
        return "F"

    def __init__(self, student_id: int, name: str, enrollment_year: int):
        self.student_id = student_id
        self.name = name
        self.enrollment_year = enrollment_year
        self.Transcript = {}

    def add_grade(self, course: str, grade: float):
        self.Transcript[course] = self.get_letter_grade(grade)

fawaz = Student(1001, "Fawaz", 2020)

fawaz.add_grade("Math", 99)
fawaz.add_grade("Science", 90.0)

print(f"Student ID: {fawaz.student_id}, Name: {fawaz.name}, Enrollment Year: {fawaz.enrollment_year}, Transcript: {fawaz.Transcript}")