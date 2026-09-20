# Student Records Manager

A command-line student records system built using pure Python and the Python standard library.

This project is Rung 0 of my KAUSTxAI Academy preparation ladder. Its purpose is to demonstrate foundational Python skills before moving into data analysis, machine learning, and neural networks.

The project covers:

* Classes and objects
* Inheritance
* Dictionaries and lists
* Properties and methods
* Input validation
* Searching and filtering
* Reading and writing CSV files
* Command-line interfaces
* Unit testing
* Organizing Python code across multiple files

No third-party packages are required.

## Project Structure

```text
Rung_0/
├── Data/
│   └── sample_students.csv
├── Tests/
│   ├── __init__.py
│   ├── test_manager.py
│   ├── test_models.py
│   └── test_storage.py
├── main.py
├── manager.py
├── models.py
├── storage.py
├── README.md
└── .gitignore
```

Each file has one main responsibility:

* `models.py` defines what a student is and what a student can do.
* `manager.py` manages the collection of student objects.
* `storage.py` saves student records to CSV and loads them again.
* `main.py` provides the interactive command-line interface.
* `Tests/` verifies that each part behaves correctly.
* `Data/` contains saved or example student records.

Separating these responsibilities makes the project easier to understand, test, and extend.

## How the Program Works

When the program starts, it follows this general process:

1. `main.py` asks `storage.py` to load existing records.
2. `storage.py` converts CSV rows into `Student` or `GraduateStudent` objects.
3. The objects are passed to `StudentManager`.
4. The user interacts with the records through the command-line menu.
5. Before exiting, the objects are converted back into CSV rows and saved.

```text
CSV file
   |
   v
storage.py
   |
   v
Student and GraduateStudent objects
   |
   v
StudentManager
   |
   v
Command-line menu
```

## The Student Model

The `Student` class represents a regular student.

Each student has:

* A unique student ID
* A name
* An enrollment year
* A transcript

The transcript is stored as a dictionary:

```python
{
    "Python": "A",
    "Mathematics": "A-"
}
```

The course name is the dictionary key, and the letter grade is its value. Dictionaries are useful here because a course can be found or updated directly using its name.

For example:

```python
student.transcript["Python"]
```

returns the grade for Python.

The `add_grade()` method accepts a numerical score:

```python
student.add_grade("Python", 95)
```

The score is validated and converted into a letter grade before being added to the transcript.

Scores below `0` or above `100` raise a `ValueError`. This prevents invalid data from entering the system.

## Grade Conversion

The grading boundaries are stored in a dictionary:

```python
scoring_system = {
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
```

The program checks the boundaries from highest to lowest. The first boundary that the score reaches determines the letter grade.

For example, a score of `91` works like this:

1. It is below `93`, so it is not an A.
2. It is at least `90`, so it is an A-.
3. The search stops after finding the correct boundary.

Checking from highest to lowest is important. If the program started at `0`, every valid score would immediately match F.

## GPA Calculation

The `gpa` property converts each letter grade into grade points:

```python
{
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
```

It then calculates the average:

```text
GPA = total grade points / number of courses
```

For an A, A-, and B+:

```text
GPA = (4.0 + 3.7 + 3.3) / 3
GPA = 3.67
```

The GPA is implemented as a property, so it can be accessed like an attribute:

```python
print(student.gpa)
```

It is calculated from the current transcript whenever it is requested. It does not need to be manually updated after a grade changes.

A student without grades receives a GPA of `0.0`.

## Inheritance

`GraduateStudent` inherits from `Student`:

```python
class GraduateStudent(Student):
```

This means a graduate student automatically receives the behavior already implemented in `Student`, including:

* Grade conversion
* Transcript management
* GPA calculation
* Student ID, name, and enrollment year

The subclass adds information specific to graduate students:

* Research topic
* Supervisor

The parent constructor is called using:

```python
super().__init__(student_id, name, enrollment_year)
```

This avoids repeating the student initialization code.

A graduate student is still considered a student:

```python
isinstance(graduate_student, Student)
```

returns `True`.

This demonstrates the main purpose of inheritance: reuse common behavior while allowing specialized classes to add their own features.

## StudentManager

`StudentManager` manages all student objects.

Students are stored in a dictionary using their IDs as keys:

```python
{
    1001: student_object,
    1002: student_object
}
```

This makes ID lookup direct:

```python
self.students.get(student_id)
```

A list would require checking students one at a time until the correct ID was found. A dictionary provides average constant-time lookup, usually written as \(O(1)\).

The manager supports:

* Adding students
* Rejecting duplicate student IDs
* Finding students by ID
* Searching by name
* Removing students
* Adding and removing grades
* Filtering by enrollment year
* Filtering by minimum GPA
* Listing graduate students

Keeping this logic inside `StudentManager` prevents the command-line interface from directly manipulating the dictionary.

## CSV Storage

The project uses Python's built-in `csv` module. Pandas is intentionally not used because this project focuses on foundational Python.

The CSV contains these columns:

```text
student_type
student_id
name
enrollment_year
research_topic
supervisor
course
letter_grade
```

Each course is stored in its own row.

For example:

```csv
student_type,student_id,name,enrollment_year,research_topic,supervisor,course,letter_grade
regular,1001,Fawaz,2026,,,Python,A
regular,1001,Fawaz,2026,,,Mathematics,A-
```

These rows do not represent duplicate students. They represent two courses belonging to the same student.

When loading the file, the program uses a dictionary indexed by student ID:

```python
students_by_id: dict[int, Student] = {}
```

The first row for student `1001` creates the student object. Later rows with the same ID add courses to that existing object.

A student with no grades still receives one row with empty course and grade fields. Without that row, there would be no record of the student in the file.

The storage system also saves a `student_type` value. This allows the loader to recreate the correct class:

```python
if row["student_type"] == "graduate":
    student = GraduateStudent(...)
else:
    student = Student(...
```
