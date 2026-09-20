from models import GraduateStudent, Student


class StudentManager:
    def __init__(self, students: list[Student] | None = None):
        self.students: dict[int, Student] = {}

        # This lets the manager start with students loaded from a CSV file.
        if students:
            for student in students:
                self.add_student(student)

    def add_student(self, student: Student) -> None:
        if student.student_id in self.students:
            raise ValueError(
                f"Student ID {student.student_id} already exists"
            )

        self.students[student.student_id] = student

    def find_student(self, student_id: int) -> Student | None:
        return self.students.get(student_id)

    def remove_student(self, student_id: int) -> Student:
        student = self.find_student(student_id)

        if student is None:
            raise KeyError(f"Student ID {student_id} was not found")

        return self.students.pop(student_id)

    def get_all_students(self) -> list[Student]:
        return sorted(
            self.students.values(),
            key=lambda student: student.student_id,
        )

    def add_grade(
        self,
        student_id: int,
        course: str,
        score: float,
    ) -> None:
        student = self.find_student(student_id)

        if student is None:
            raise KeyError(f"Student ID {student_id} was not found")

        student.add_grade(course, score)

    def remove_grade(self, student_id: int, course: str) -> None:
        student = self.find_student(student_id)

        if student is None:
            raise KeyError(f"Student ID {student_id} was not found")

        student.remove_grade(course)

    def filter_by_enrollment_year(
        self,
        enrollment_year: int,
    ) -> list[Student]:
        return [
            student
            for student in self.get_all_students()
            if student.enrollment_year == enrollment_year
        ]

    def filter_by_minimum_gpa(
        self,
        minimum_gpa: float,
    ) -> list[Student]:
        if minimum_gpa < 0 or minimum_gpa > 4:
            raise ValueError("Minimum GPA must be between 0 and 4")

        return [
            student
            for student in self.get_all_students()
            if student.gpa >= minimum_gpa
        ]

    def find_by_name(self, name: str) -> list[Student]:
        search_term = name.strip().lower()

        if not search_term:
            return []

        return [
            student
            for student in self.get_all_students()
            if search_term in student.name.lower()
        ]

    def get_graduate_students(self) -> list[GraduateStudent]:
        return [
            student
            for student in self.get_all_students()
            if isinstance(student, GraduateStudent)
        ]

    def student_count(self) -> int:
        return len(self.students)