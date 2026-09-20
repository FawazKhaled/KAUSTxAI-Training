import unittest

from models import GraduateStudent, Student


class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student = Student(
            student_id=1001,
            name="Fawaz Alharbi",
            enrollment_year=2026,
        )

    def test_student_is_created_correctly(self):
        self.assertEqual(self.student.student_id, 1001)
        self.assertEqual(self.student.name, "Fawaz Alharbi")
        self.assertEqual(self.student.enrollment_year, 2026)
        self.assertEqual(self.student.transcript, {})

    def test_student_name_is_stripped(self):
        student = Student(
            student_id=1002,
            name="  Ahmed Ali  ",
            enrollment_year=2026,
        )

        self.assertEqual(student.name, "Ahmed Ali")

    def test_invalid_student_id_is_rejected(self):
        with self.assertRaises(ValueError):
            Student(0, "Fawaz", 2026)

        with self.assertRaises(ValueError):
            Student(-1, "Fawaz", 2026)

    def test_empty_student_name_is_rejected(self):
        with self.assertRaises(ValueError):
            Student(1001, "", 2026)

        with self.assertRaises(ValueError):
            Student(1001, "   ", 2026)

    def test_invalid_enrollment_year_is_rejected(self):
        with self.assertRaises(ValueError):
            Student(1001, "Fawaz", 0)

        with self.assertRaises(ValueError):
            Student(1001, "Fawaz", -2026)

    def test_grade_boundaries(self):
        test_cases = [
            (100, "A"),
            (93, "A"),
            (92.99, "A-"),
            (90, "A-"),
            (89.99, "B+"),
            (87, "B+"),
            (83, "B"),
            (80, "B-"),
            (77, "C+"),
            (73, "C"),
            (70, "C-"),
            (60, "D"),
            (59.99, "F"),
            (0, "F"),
        ]

        for score, expected_grade in test_cases:
            with self.subTest(score=score):
                actual_grade = self.student.get_letter_grade(score)

                self.assertEqual(
                    actual_grade,
                    expected_grade,
                )

    def test_score_above_100_is_rejected(self):
        with self.assertRaises(ValueError):
            self.student.get_letter_grade(100.01)

    def test_score_below_zero_is_rejected(self):
        with self.assertRaises(ValueError):
            self.student.get_letter_grade(-0.01)

    def test_add_grade(self):
        self.student.add_grade("Python", 95)

        self.assertEqual(
            self.student.transcript["Python"],
            "A",
        )

    def test_course_name_is_stripped(self):
        self.student.add_grade("  Python  ", 95)

        self.assertIn("Python", self.student.transcript)
        self.assertNotIn("  Python  ", self.student.transcript)

    def test_empty_course_name_is_rejected(self):
        with self.assertRaises(ValueError):
            self.student.add_grade("", 95)

        with self.assertRaises(ValueError):
            self.student.add_grade("   ", 95)

    def test_existing_grade_can_be_updated(self):
        self.student.add_grade("Python", 70)
        self.student.add_grade("Python", 95)

        self.assertEqual(
            self.student.transcript["Python"],
            "A",
        )

        self.assertEqual(len(self.student.transcript), 1)

    def test_get_existing_grade(self):
        self.student.add_grade("Python", 95)

        self.assertEqual(
            self.student.get_grade("Python"),
            "A",
        )

    def test_get_missing_grade_returns_none(self):
        self.assertIsNone(
            self.student.get_grade("Python")
        )

    def test_remove_grade(self):
        self.student.add_grade("Python", 95)
        self.student.remove_grade("Python")

        self.assertNotIn(
            "Python",
            self.student.transcript,
        )

    def test_remove_missing_grade_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.student.remove_grade("Python")

    def test_gpa_is_zero_without_grades(self):
        self.assertEqual(self.student.gpa, 0.0)

    def test_gpa_is_calculated_correctly(self):
        self.student.add_grade("Python", 95)
        self.student.add_grade("Mathematics", 90)
        self.student.add_grade("Statistics", 87)

        # A, A- and B+ give an average GPA of 3.67.
        self.assertEqual(self.student.gpa, 3.67)

    def test_gpa_changes_when_grade_is_updated(self):
        self.student.add_grade("Python", 70)
        self.assertEqual(self.student.gpa, 1.7)

        self.student.add_grade("Python", 95)
        self.assertEqual(self.student.gpa, 4.0)

    def test_student_string_contains_main_information(self):
        student_text = str(self.student)

        self.assertIn("1001", student_text)
        self.assertIn("Fawaz Alharbi", student_text)
        self.assertIn("2026", student_text)
        self.assertIn("GPA: 0.00", student_text)


class TestGraduateStudent(unittest.TestCase):
    def setUp(self):
        self.student = GraduateStudent(
            student_id=2001,
            name="Sara Mohammed",
            enrollment_year=2025,
            research_topic="Machine Learning",
            supervisor="Dr. Abdullah",
        )

    def test_graduate_student_inherits_from_student(self):
        self.assertIsInstance(self.student, Student)
        self.assertIsInstance(
            self.student,
            GraduateStudent,
        )

    def test_graduate_student_information(self):
        self.assertEqual(
            self.student.research_topic,
            "Machine Learning",
        )

        self.assertEqual(
            self.student.supervisor,
            "Dr. Abdullah",
        )

    def test_graduate_student_can_use_student_methods(self):
        self.student.add_grade("Python", 95)

        self.assertEqual(
            self.student.transcript["Python"],
            "A",
        )

        self.assertEqual(self.student.gpa, 4.0)

    def test_supervisor_is_optional(self):
        student = GraduateStudent(
            student_id=2002,
            name="Ahmed Ali",
            enrollment_year=2025,
            research_topic="Cybersecurity",
        )

        self.assertIsNone(student.supervisor)

    def test_assign_supervisor(self):
        self.student.assign_supervisor("Dr. Khalid")

        self.assertEqual(
            self.student.supervisor,
            "Dr. Khalid",
        )

    def test_supervisor_name_is_stripped(self):
        self.student.assign_supervisor("  Dr. Khalid  ")

        self.assertEqual(
            self.student.supervisor,
            "Dr. Khalid",
        )

    def test_empty_supervisor_is_rejected(self):
        with self.assertRaises(ValueError):
            self.student.assign_supervisor("")

        with self.assertRaises(ValueError):
            self.student.assign_supervisor("   ")

    def test_empty_research_topic_is_rejected(self):
        with self.assertRaises(ValueError):
            GraduateStudent(
                student_id=2002,
                name="Ahmed Ali",
                enrollment_year=2025,
                research_topic="",
            )

    def test_graduate_student_string_has_research_details(self):
        student_text = str(self.student)

        self.assertIn("Machine Learning", student_text)
        self.assertIn("Dr. Abdullah", student_text)


if __name__ == "__main__":
    unittest.main()