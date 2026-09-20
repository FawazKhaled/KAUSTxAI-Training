import unittest

from manager import StudentManager
from models import GraduateStudent, Student


class TestStudentManager(unittest.TestCase):
    def setUp(self):
        # These objects are recreated before every test.
        self.manager = StudentManager()

        self.fawaz = Student(
            student_id=1001,
            name="Fawaz Alharbi",
            enrollment_year=2026,
        )

        self.ahmed = Student(
            student_id=1002,
            name="Ahmed Ali",
            enrollment_year=2025,
        )

        self.sara = GraduateStudent(
            student_id=1003,
            name="Sara Mohammed",
            enrollment_year=2026,
            research_topic="Machine Learning",
            supervisor="Dr. Abdullah",
        )

    def test_manager_starts_empty(self):
        self.assertEqual(self.manager.student_count(), 0)
        self.assertEqual(self.manager.get_all_students(), [])

    def test_manager_can_start_with_students(self):
        manager = StudentManager([self.fawaz, self.ahmed])

        self.assertEqual(manager.student_count(), 2)
        self.assertIs(manager.find_student(1001), self.fawaz)
        self.assertIs(manager.find_student(1002), self.ahmed)

    def test_add_student(self):
        self.manager.add_student(self.fawaz)

        self.assertEqual(self.manager.student_count(), 1)
        self.assertIs(
            self.manager.find_student(1001),
            self.fawaz,
        )

    def test_duplicate_student_id_is_rejected(self):
        self.manager.add_student(self.fawaz)

        duplicate = Student(
            student_id=1001,
            name="Different Student",
            enrollment_year=2024,
        )

        with self.assertRaises(ValueError):
            self.manager.add_student(duplicate)

    def test_find_missing_student_returns_none(self):
        result = self.manager.find_student(9999)

        self.assertIsNone(result)

    def test_remove_student(self):
        self.manager.add_student(self.fawaz)

        removed_student = self.manager.remove_student(1001)

        self.assertIs(removed_student, self.fawaz)
        self.assertIsNone(self.manager.find_student(1001))
        self.assertEqual(self.manager.student_count(), 0)

    def test_removing_missing_student_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.manager.remove_student(9999)

    def test_get_all_students_sorts_by_id(self):
        self.manager.add_student(self.sara)
        self.manager.add_student(self.fawaz)
        self.manager.add_student(self.ahmed)

        students = self.manager.get_all_students()
        student_ids = [
            student.student_id for student in students
        ]

        self.assertEqual(student_ids, [1001, 1002, 1003])

    def test_add_grade_to_student(self):
        self.manager.add_student(self.fawaz)

        self.manager.add_grade(
            student_id=1001,
            course="Python",
            score=95,
        )

        self.assertEqual(
            self.fawaz.transcript["Python"],
            "A",
        )

    def test_add_grade_to_missing_student_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.manager.add_grade(
                student_id=9999,
                course="Python",
                score=95,
            )

    def test_remove_grade_from_student(self):
        self.fawaz.add_grade("Python", 95)
        self.manager.add_student(self.fawaz)

        self.manager.remove_grade(1001, "Python")

        self.assertNotIn("Python", self.fawaz.transcript)

    def test_filter_by_enrollment_year(self):
        self.manager.add_student(self.fawaz)
        self.manager.add_student(self.ahmed)
        self.manager.add_student(self.sara)

        matches = self.manager.filter_by_enrollment_year(2026)

        self.assertEqual(
            [student.student_id for student in matches],
            [1001, 1003],
        )

    def test_filter_by_minimum_gpa(self):
        self.fawaz.add_grade("Python", 95)
        self.ahmed.add_grade("Python", 75)

        self.manager.add_student(self.fawaz)
        self.manager.add_student(self.ahmed)

        matches = self.manager.filter_by_minimum_gpa(3.0)

        self.assertEqual(matches, [self.fawaz])

    def test_invalid_minimum_gpa_is_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.filter_by_minimum_gpa(4.5)

        with self.assertRaises(ValueError):
            self.manager.filter_by_minimum_gpa(-1)

    def test_find_by_name_is_case_insensitive(self):
        self.manager.add_student(self.fawaz)
        self.manager.add_student(self.ahmed)

        matches = self.manager.find_by_name("fAwAz")

        self.assertEqual(matches, [self.fawaz])

    def test_find_by_partial_name(self):
        self.manager.add_student(self.fawaz)

        matches = self.manager.find_by_name("alhar")

        self.assertEqual(matches, [self.fawaz])

    def test_empty_name_search_returns_empty_list(self):
        self.manager.add_student(self.fawaz)

        self.assertEqual(self.manager.find_by_name(""), [])
        self.assertEqual(self.manager.find_by_name("   "), [])

    def test_get_graduate_students(self):
        self.manager.add_student(self.fawaz)
        self.manager.add_student(self.sara)

        graduate_students = (
            self.manager.get_graduate_students()
        )

        self.assertEqual(graduate_students, [self.sara])
        self.assertIsInstance(
            graduate_students[0],
            GraduateStudent,
        )


if __name__ == "__main__":
    unittest.main()