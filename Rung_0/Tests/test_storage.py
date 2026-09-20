import csv
import tempfile
import unittest
from pathlib import Path

from models import GraduateStudent, Student
from storage import load_students, save_students


class TestStorage(unittest.TestCase):
    def setUp(self):
        # Each test gets its own temporary folder.
        self.temporary_folder = tempfile.TemporaryDirectory()
        self.csv_file = (
            Path(self.temporary_folder.name) / "students.csv"
        )

        self.fawaz = Student(
            student_id=1001,
            name="Fawaz Alharbi",
            enrollment_year=2026,
        )
        self.fawaz.add_grade("Python", 95)
        self.fawaz.add_grade("Mathematics", 90)

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
        self.sara.add_grade("Statistics", 87)

    def tearDown(self):
        # This removes the temporary folder after every test.
        self.temporary_folder.cleanup()

    def test_missing_file_returns_empty_list(self):
        missing_file = (
            Path(self.temporary_folder.name) / "missing.csv"
        )

        students = load_students(str(missing_file))

        self.assertEqual(students, [])

    def test_save_students_creates_csv_file(self):
        save_students(
            [self.fawaz],
            str(self.csv_file),
        )

        self.assertTrue(self.csv_file.exists())

    def test_csv_contains_expected_header(self):
        save_students(
            [self.fawaz],
            str(self.csv_file),
        )

        with open(
            self.csv_file,
            "r",
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.reader(file)
            header = next(reader)

        self.assertEqual(
            header,
            [
                "student_type",
                "student_id",
                "name",
                "enrollment_year",
                "research_topic",
                "supervisor",
                "course",
                "letter_grade",
            ],
        )

    def test_save_and_load_regular_student(self):
        save_students(
            [self.fawaz],
            str(self.csv_file),
        )

        loaded_students = load_students(
            str(self.csv_file)
        )

        self.assertEqual(len(loaded_students), 1)

        loaded_student = loaded_students[0]

        self.assertIsInstance(loaded_student, Student)
        self.assertNotIsInstance(
            loaded_student,
            GraduateStudent,
        )
        self.assertEqual(loaded_student.student_id, 1001)
        self.assertEqual(
            loaded_student.name,
            "Fawaz Alharbi",
        )
        self.assertEqual(
            loaded_student.enrollment_year,
            2026,
        )

    def test_transcript_is_preserved(self):
        save_students(
            [self.fawaz],
            str(self.csv_file),
        )

        loaded_student = load_students(
            str(self.csv_file)
        )[0]

        self.assertEqual(
            loaded_student.transcript,
            {
                "Python": "A",
                "Mathematics": "A-",
            },
        )

        self.assertEqual(loaded_student.gpa, 3.85)

    def test_student_without_grades_is_preserved(self):
        save_students(
            [self.ahmed],
            str(self.csv_file),
        )

        loaded_students = load_students(
            str(self.csv_file)
        )

        self.assertEqual(len(loaded_students), 1)
        self.assertEqual(
            loaded_students[0].student_id,
            1002,
        )
        self.assertEqual(
            loaded_students[0].transcript,
            {},
        )
        self.assertEqual(
            loaded_students[0].gpa,
            0.0,
        )

    def test_graduate_student_is_preserved(self):
        save_students(
            [self.sara],
            str(self.csv_file),
        )

        loaded_student = load_students(
            str(self.csv_file)
        )[0]

        self.assertIsInstance(
            loaded_student,
            GraduateStudent,
        )

        self.assertEqual(
            loaded_student.research_topic,
            "Machine Learning",
        )

        self.assertEqual(
            loaded_student.supervisor,
            "Dr. Abdullah",
        )

        self.assertEqual(
            loaded_student.transcript,
            {"Statistics": "B+"},
        )

    def test_graduate_student_without_supervisor(self):
        graduate_student = GraduateStudent(
            student_id=1004,
            name="Khalid Hassan",
            enrollment_year=2026,
            research_topic="Cybersecurity",
        )

        save_students(
            [graduate_student],
            str(self.csv_file),
        )

        loaded_student = load_students(
            str(self.csv_file)
        )[0]

        self.assertIsInstance(
            loaded_student,
            GraduateStudent,
        )
        self.assertIsNone(loaded_student.supervisor)

    def test_multiple_students_are_preserved(self):
        students = [
            self.fawaz,
            self.ahmed,
            self.sara,
        ]

        save_students(students, str(self.csv_file))

        loaded_students = load_students(
            str(self.csv_file)
        )

        students_by_id = {
            student.student_id: student
            for student in loaded_students
        }

        self.assertEqual(len(students_by_id), 3)
        self.assertIn(1001, students_by_id)
        self.assertIn(1002, students_by_id)
        self.assertIn(1003, students_by_id)

        self.assertIsInstance(
            students_by_id[1003],
            GraduateStudent,
        )

    def test_student_with_multiple_courses_is_loaded_once(self):
        save_students(
            [self.fawaz],
            str(self.csv_file),
        )

        loaded_students = load_students(
            str(self.csv_file)
        )

        self.assertEqual(len(loaded_students), 1)
        self.assertEqual(
            len(loaded_students[0].transcript),
            2,
        )

    def test_saving_again_replaces_old_file_contents(self):
        save_students(
            [self.fawaz],
            str(self.csv_file),
        )

        save_students(
            [self.ahmed],
            str(self.csv_file),
        )

        loaded_students = load_students(
            str(self.csv_file)
        )

        self.assertEqual(len(loaded_students), 1)
        self.assertEqual(
            loaded_students[0].student_id,
            1002,
        )

    def test_empty_student_list_creates_header_only_file(self):
        save_students([], str(self.csv_file))

        loaded_students = load_students(
            str(self.csv_file)
        )

        self.assertEqual(loaded_students, [])
        self.assertTrue(self.csv_file.exists())

    def test_unknown_student_type_is_rejected(self):
        with open(
            self.csv_file,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "student_type",
                    "student_id",
                    "name",
                    "enrollment_year",
                    "research_topic",
                    "supervisor",
                    "course",
                    "letter_grade",
                ],
            )

            writer.writeheader()
            writer.writerow({
                "student_type": "unknown",
                "student_id": 9999,
                "name": "Invalid Student",
                "enrollment_year": 2026,
                "research_topic": "",
                "supervisor": "",
                "course": "",
                "letter_grade": "",
            })

        with self.assertRaises(ValueError):
            load_students(str(self.csv_file))


if __name__ == "__main__":
    unittest.main()