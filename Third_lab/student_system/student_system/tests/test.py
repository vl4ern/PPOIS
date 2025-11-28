import sys
import os

# Добавляем корневую директорию проекта в sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Поднимаемся на уровень выше tests
sys.path.insert(0, project_root)

import unittest
from system.models.Academic.Requirement import Requirement
from system.models.Academic.GradeScale import GradeScale
from system.models.Academic.Degree import Degree
from system.models.Academic.Program import Program
from system.models.Academic.Exam import Exam

from system.models.Additional.Badge import Badge
from system.models.Additional.Event import Event
from system.models.Additional.Notification import Notification
from system.models.Additional.RecoveryToken import RecoveryToken
from system.models.Additional.RolePerm import RolePerm

from system.models.Course.Course import Course
from system.models.Course.CourseSchedule import CourseSchedule
from system.models.Course.Module import Module
from system.models.Course.Syllabus import Syllabus

from system.models.Finance.Account import Account
from system.models.Finance.Transaction import Transaction
from system.models.Finance.Scholarship import Scholarship
from system.models.Finance.Card import Card
from system.models.Finance.Billing import Billing

from system.models.Housing.Dorm import Dorm
from system.models.Housing.Lease import Lease
from system.models.Housing.MaintenanceReauest import MaintenanceRequest
from system.models.Housing.Room import Room

from system.models.Library.Library import Library
from system.models.Library.Author import Author
from system.models.Library.Book import Book
from system.models.Library.BorrowRecord import BorrowRecord

from system.models.Person.Person import Person
from system.models.Person.IDCard import IDCard
from system.models.Person.Address import Address
from system.models.Person.ContactInfo import ContactInfo

from system.models.Schedule.CalendarEntry import CalendarEntry
from system.models.Schedule.Scheduler import Scheduler
from system.models.Schedule.TimeSlot import TimeSlot

from system.models.Student.Student import Student
from system.models.Student.CalendarEntry import CalendarEntry
from system.models.Student.EnrollmentRecord import EnrollmentRecord
from system.models.Student.GradeRecord import GradeRecord
from system.models.Student.Transcript import Transcript

from system.models.Teacher.Teacher import Teacher
from system.models.Teacher.Office import Office
from system.models.Teacher.Qualification import Qualification

from system.models.University.University import University
from system.models.University.Campus import Campus
from system.models.University.Department import Department
from system.models.University.Faculty import Faculty

class TestFaculty(unittest.TestCase):
    def test_faculty_initialization(self):
        faculty = Faculty("Faculty of Science", "Dr. John Smith")
        self.assertEqual(faculty.name, "Faculty of Science")
        self.assertEqual(faculty.dean, "Dr. John Smith")
    
    def test_faculty_initialization_default_dean(self):
        faculty = Faculty("Faculty of Arts")
        self.assertEqual(faculty.name, "Faculty of Arts")
        self.assertEqual(faculty.dean, "")
    
    def test_faculty_edge_cases(self):
        # Empty name
        faculty = Faculty("", "Dr. Unknown")
        self.assertEqual(faculty.name, "")
        self.assertEqual(faculty.dean, "Dr. Unknown")
        
        # Very long names
        long_name = "A" * 100
        long_dean = "B" * 100
        faculty = Faculty(long_name, long_dean)
        self.assertEqual(faculty.name, long_name)
        self.assertEqual(faculty.dean, long_dean)


class TestDepartment(unittest.TestCase):
    def test_department_initialization(self):
        department = Department("Computer Science", "Prof. Alice Johnson")
        self.assertEqual(department.name, "Computer Science")
        self.assertEqual(department.head, "Prof. Alice Johnson")
        self.assertEqual(department.courses, [])
    
    def test_department_initialization_default_head(self):
        department = Department("Mathematics")
        self.assertEqual(department.name, "Mathematics")
        self.assertIsNone(department.head)
        self.assertEqual(department.courses, [])
    
    def test_department_add_course(self):
        department = Department("Physics")
        course = "PHY101 - Introduction to Physics"
        
        department.add_course(course)
        
        self.assertEqual(len(department.courses), 1)
        self.assertEqual(department.courses[0], course)
    
    def test_department_add_multiple_courses(self):
        department = Department("Chemistry")
        
        courses = [
            "CHEM101 - General Chemistry",
            "CHEM102 - Organic Chemistry", 
            "CHEM201 - Analytical Chemistry"
        ]
        
        for course in courses:
            department.add_course(course)
        
        self.assertEqual(len(department.courses), 3)
        self.assertEqual(department.courses, courses)
    
    def test_department_add_different_course_types(self):
        department = Department("Engineering")
        
        # Test with string courses
        string_course = "ENG101"
        department.add_course(string_course)
        
        # Test with object courses
        class Course:
            def __init__(self, code, title):
                self.code = code
                self.title = title
        
        course_obj = Course("ENG202", "Advanced Engineering")
        department.add_course(course_obj)
        
        self.assertEqual(len(department.courses), 2)
        self.assertEqual(department.courses[0], string_course)
        self.assertEqual(department.courses[1], course_obj)
    
    def test_department_edge_cases(self):
        # Empty department name
        department = Department("")
        self.assertEqual(department.name, "")
        self.assertIsNone(department.head)
        
        # Add empty course
        department.add_course("")
        self.assertEqual(len(department.courses), 1)
        self.assertEqual(department.courses[0], "")


class TestCampus(unittest.TestCase):
    def test_campus_initialization(self):
        campus = Campus("Downtown Campus", 5000)
        self.assertEqual(campus.location, "Downtown Campus")
        self.assertEqual(campus.capacity, 5000)
    
    def test_campus_initialization_default_capacity(self):
        campus = Campus("North Campus")
        self.assertEqual(campus.location, "North Campus")
        self.assertEqual(campus.capacity, 1000)  # default value
    
    def test_campus_edge_cases(self):
        # Empty location
        campus = Campus("", 100)
        self.assertEqual(campus.location, "")
        self.assertEqual(campus.capacity, 100)
        
        # Zero capacity
        campus = Campus("Small Campus", 0)
        self.assertEqual(campus.capacity, 0)
        
        # Very large capacity
        campus = Campus("Mega Campus", 1000000)
        self.assertEqual(campus.capacity, 1000000)
        
        # Negative capacity (if allowed by business logic)
        campus = Campus("Test Campus", -100)
        self.assertEqual(campus.capacity, -100)


class TestUniversity(unittest.TestCase):
    def test_university_initialization(self):
        university = University("State University")
        self.assertEqual(university.name, "State University")
        self.assertEqual(university.departments, [])
        self.assertEqual(university.campuses, [])
    
    def test_university_add_department(self):
        university = University("Test University")
        department = Department("Computer Science")
        
        university.add_department(department)
        
        self.assertEqual(len(university.departments), 1)
        self.assertEqual(university.departments[0], department)
    
    def test_university_add_multiple_departments(self):
        university = University("Multi-Department University")
        
        departments = [
            Department("Mathematics"),
            Department("Physics"),
            Department("Chemistry"),
            Department("Biology")
        ]
        
        for department in departments:
            university.add_department(department)
        
        self.assertEqual(len(university.departments), 4)
        self.assertEqual(university.departments[0].name, "Mathematics")
        self.assertEqual(university.departments[1].name, "Physics")
        self.assertEqual(university.departments[2].name, "Chemistry")
        self.assertEqual(university.departments[3].name, "Biology")
    
    def test_university_find_course_existing(self):
        university = University("Search University")
        
        # Create departments with courses
        cs_dept = Department("Computer Science")
        math_dept = Department("Mathematics")
        
        # Create mock courses with code attribute
        class MockCourse:
            def __init__(self, code, title):
                self.code = code
                self.title = title
        
        cs_courses = [
            MockCourse("CS101", "Introduction to Programming"),
            MockCourse("CS201", "Data Structures"),
            MockCourse("CS301", "Algorithms")
        ]
        
        math_courses = [
            MockCourse("MATH101", "Calculus I"),
            MockCourse("MATH201", "Linear Algebra")
        ]
        
        # Add courses to departments
        for course in cs_courses:
            cs_dept.add_course(course)
        
        for course in math_courses:
            math_dept.add_course(course)
        
        # Add departments to university
        university.add_department(cs_dept)
        university.add_department(math_dept)
        
        # Test finding existing courses
        found_course = university.find_course("CS201")
        self.assertIsNotNone(found_course)
        self.assertEqual(found_course.code, "CS201")
        self.assertEqual(found_course.title, "Data Structures")
        
        found_math_course = university.find_course("MATH101")
        self.assertIsNotNone(found_math_course)
        self.assertEqual(found_math_course.code, "MATH101")
    
    def test_university_find_course_non_existing(self):
        university = University("Empty University")
        
        # Test with no departments
        result = university.find_course("ANY101")
        self.assertIsNone(result)
        
        # Test with departments but no matching course
        dept = Department("Test Department")
        
        class MockCourse:
            def __init__(self, code):
                self.code = code
        
        dept.add_course(MockCourse("EXIST101"))
        university.add_department(dept)
        
        result = university.find_course("NONEXIST101")
        self.assertIsNone(result)
    
    def test_university_find_course_multiple_departments(self):
        university = University("Large University")
        
        # Create multiple departments with some overlapping course codes
        dept1 = Department("Engineering")
        dept2 = Department("Computer Science")
        
        class MockCourse:
            def __init__(self, code, title):
                self.code = code
                self.title = title
        
        # Both departments have a course with code "PROG101"
        eng_course = MockCourse("PROG101", "Engineering Programming")
        cs_course = MockCourse("PROG101", "Introduction to Programming")
        
        dept1.add_course(eng_course)
        dept2.add_course(cs_course)
        
        university.add_department(dept1)
        university.add_department(dept2)
        
        # Should return the first match found (from Engineering department)
        found = university.find_course("PROG101")
        self.assertIsNotNone(found)
        self.assertEqual(found.title, "Engineering Programming")
    
    def test_university_find_course_empty_code(self):
        university = University("Test University")
        dept = Department("Test Dept")
        
        class MockCourse:
            def __init__(self, code):
                self.code = code
        
        dept.add_course(MockCourse(""))
        dept.add_course(MockCourse("CS101"))
        
        university.add_department(dept)
        
        # Search for empty code
        result = university.find_course("")
        self.assertIsNotNone(result)
        self.assertEqual(result.code, "")
    
    def test_university_campus_management(self):
        university = University("Multi-Campus University")
        
        campuses = [
            Campus("Main Campus", 10000),
            Campus("Downtown Campus", 5000),
            Campus("North Campus", 3000)
        ]
        
        # Add campuses to university
        university.campuses.extend(campuses)
        
        self.assertEqual(len(university.campuses), 3)
        self.assertEqual(university.campuses[0].location, "Main Campus")
        self.assertEqual(university.campuses[1].capacity, 5000)
        self.assertEqual(university.campuses[2].location, "North Campus")
    
    def test_university_edge_cases(self):
        # University with empty name
        university = University("")
        self.assertEqual(university.name, "")
        
        # Add department with None
        university.add_department(None)
        self.assertEqual(len(university.departments), 1)
        self.assertIsNone(university.departments[0])
        
        # Find course in university with None departments
        university_with_none = University("Test")
        university_with_none.departments = [None]
        result = university_with_none.find_course("ANY")
        self.assertIsNone(result)


class TestUniversityIntegration(unittest.TestCase):
    def test_complete_university_structure(self):
        # Create a university
        university = University("National University")
        
        # Create faculties
        science_faculty = Faculty("Faculty of Science", "Dr. Marie Curie")
        arts_faculty = Faculty("Faculty of Arts", "Dr. William Shakespeare")
        
        # Create departments
        cs_dept = Department("Computer Science", "Prof. Alan Turing")
        math_dept = Department("Mathematics", "Prof. Isaac Newton")
        physics_dept = Department("Physics", "Prof. Albert Einstein")
        english_dept = Department("English", "Prof. Jane Austen")
        
        # Create mock courses
        class Course:
            def __init__(self, code, title):
                self.code = code
                self.title = title
        
        # Add courses to science departments
        cs_courses = [
            Course("CS101", "Programming Fundamentals"),
            Course("CS201", "Data Structures"),
            Course("CS301", "Algorithms and Complexity")
        ]
        
        math_courses = [
            Course("MATH101", "Calculus I"),
            Course("MATH201", "Linear Algebra"),
            Course("MATH301", "Differential Equations")
        ]
        
        physics_courses = [
            Course("PHY101", "Classical Mechanics"),
            Course("PHY201", "Electromagnetism"),
            Course("PHY301", "Quantum Physics")
        ]
        
        # Add courses to arts departments
        english_courses = [
            Course("ENG101", "Introduction to Literature"),
            Course("ENG201", "Shakespeare Studies"),
            Course("ENG301", "Modern Poetry")
        ]
        
        for course in cs_courses:
            cs_dept.add_course(course)
        
        for course in math_courses:
            math_dept.add_course(course)
            
        for course in physics_courses:
            physics_dept.add_course(course)
            
        for course in english_courses:
            english_dept.add_course(course)
        
        # Add departments to university
        university.add_department(cs_dept)
        university.add_department(math_dept)
        university.add_department(physics_dept)
        university.add_department(english_dept)
        
        # Create campuses
        main_campus = Campus("Main Campus", 15000)
        downtown_campus = Campus("Downtown Campus", 5000)
        
        university.campuses.append(main_campus)
        university.campuses.append(downtown_campus)
        
        # Verify university structure
        self.assertEqual(university.name, "National University")
        self.assertEqual(len(university.departments), 4)
        self.assertEqual(len(university.campuses), 2)
        
        # Test course search functionality
        found_course = university.find_course("CS201")
        self.assertIsNotNone(found_course)
        self.assertEqual(found_course.title, "Data Structures")
        
        found_english_course = university.find_course("ENG301")
        self.assertIsNotNone(found_english_course)
        self.assertEqual(found_english_course.title, "Modern Poetry")
        
        # Test non-existing course
        non_existing = university.find_course("NONEXIST999")
        self.assertIsNone(non_existing)
        
        # Verify campus information
        self.assertEqual(university.campuses[0].location, "Main Campus")
        self.assertEqual(university.campuses[1].capacity, 5000)
        
        # Verify department information
        self.assertEqual(cs_dept.head, "Prof. Alan Turing")
        self.assertEqual(len(math_dept.courses), 3)
        self.assertEqual(english_dept.courses[0].code, "ENG101")


class TestOffice(unittest.TestCase):
    def test_office_initialization(self):
        office = Office("Science Building", "Room 205", "+1234567890")
        self.assertEqual(office.building, "Science Building")
        self.assertEqual(office.room, "Room 205")
        self.assertEqual(office.phone, "+1234567890")
    
    def test_office_initialization_default_phone(self):
        office = Office("Arts Building", "Room 101")
        self.assertEqual(office.building, "Arts Building")
        self.assertEqual(office.room, "Room 101")
        self.assertEqual(office.phone, "")
    
    def test_office_location(self):
        office = Office("Engineering", "E-305", "+0987654321")
        location = office.location()
        expected = "Engineering E-305"
        self.assertEqual(location, expected)
    
    def test_office_location_special_characters(self):
        office = Office("St. John's Hall", "Room 1-A", "")
        location = office.location()
        expected = "St. John's Hall Room 1-A"
        self.assertEqual(location, expected)
    
    def test_office_location_empty_fields(self):
        office = Office("", "", "")
        location = office.location()
        expected = " "
        self.assertEqual(location, expected)
    
    def test_office_location_partial_empty(self):
        office = Office("", "B-12", "")
        location = office.location()
        expected = "  B-12"
        self.assertEqual(location, expected)


class TestQualification(unittest.TestCase):
    def test_qualification_initialization(self):
        qualification = Qualification("PhD in Computer Science", "MIT", 2015)
        self.assertEqual(qualification.title, "PhD in Computer Science")
        self.assertEqual(qualification.institution, "MIT")
        self.assertEqual(qualification.year, 2015)
    
    def test_qualification_short(self):
        qualification = Qualification("MSc in Mathematics", "Stanford University", 2010)
        short_form = qualification.short()
        expected = "MSc in Mathematics (2010)"
        self.assertEqual(short_form, expected)
    
    def test_qualification_short_special_years(self):
        # Test with early year
        early_qual = Qualification("BSc", "Harvard", 1900)
        self.assertEqual(early_qual.short(), "BSc (1900)")
        
        # Test with future year
        future_qual = Qualification("PostDoc", "Cambridge", 2030)
        self.assertEqual(future_qual.short(), "PostDoc (2030)")
    
    def test_qualification_short_special_titles(self):
        test_cases = [
            ("", "Test Institution", 2000),  # Empty title
            ("A" * 100, "Short Inst", 1999),  # Very long title
            ("B.A. (Hons)", "Oxford", 2012),  # Special characters
        ]
        
        for title, institution, year in test_cases:
            qual = Qualification(title, institution, year)
            expected = f"{title} ({year})"
            self.assertEqual(qual.short(), expected)


class TestTeacher(unittest.TestCase):
    def test_teacher_initialization(self):
        teacher = Teacher("John", "Smith", "T12345", "john.smith@university.edu")
        
        self.assertEqual(teacher.first_name, "John")
        self.assertEqual(teacher.last_name, "Smith")
        self.assertEqual(teacher.teacher_id, "T12345")
        self.assertEqual(teacher.email, "john.smith@university.edu")
        self.assertEqual(teacher.courses, [])
        self.assertIsNone(teacher.office)
        self.assertEqual(teacher.qualifications, [])
    
    def test_teacher_initialization_default_email(self):
        teacher = Teacher("Jane", "Doe", "T67890")
        
        self.assertEqual(teacher.first_name, "Jane")
        self.assertEqual(teacher.last_name, "Doe")
        self.assertEqual(teacher.teacher_id, "T67890")
        self.assertEqual(teacher.email, "")
        self.assertEqual(teacher.courses, [])
    
    def test_teacher_inheritance_from_person(self):
        teacher = Teacher("Robert", "Brown", "T11111", "robert@university.edu")
        
        # Test inherited methods
        self.assertEqual(teacher.full_name(), "Robert Brown")
        
        contact_card = teacher.contact_card()
        expected_contact = {
            "name": "Robert Brown",
            "email": "robert@university.edu",
            "phone": ""  # Phone not set in Teacher initialization
        }
        self.assertEqual(contact_card, expected_contact)
    
    def test_teacher_add_course(self):
        teacher = Teacher("Alice", "Johnson", "T22222")
        
        # Test adding string courses
        course1 = "CS101"
        teacher.add_course(course1)
        self.assertEqual(len(teacher.courses), 1)
        self.assertEqual(teacher.courses[0], course1)
        
        # Test adding object courses
        class Course:
            def __init__(self, code, title):
                self.code = code
                self.title = title
        
        course_obj = Course("MATH202", "Advanced Mathematics")
        teacher.add_course(course_obj)
        self.assertEqual(len(teacher.courses), 2)
        self.assertEqual(teacher.courses[1], course_obj)
    
    def test_teacher_add_multiple_courses(self):
        teacher = Teacher("Bob", "Wilson", "T33333")
        
        courses = ["PHY101", "CHEM101", "BIO101", "ENG101"]
        
        for course in courses:
            teacher.add_course(course)
        
        self.assertEqual(len(teacher.courses), 4)
        self.assertEqual(teacher.courses, courses)
    
    def test_teacher_remove_course_existing(self):
        teacher = Teacher("Carol", "Davis", "T44444")
        
        courses = ["CS101", "CS102", "CS201"]
        for course in courses:
            teacher.add_course(course)
        
        self.assertEqual(len(teacher.courses), 3)
        
        # Remove existing course
        teacher.remove_course("CS102")
        self.assertEqual(len(teacher.courses), 2)
        self.assertEqual(teacher.courses, ["CS101", "CS201"])
    
    def test_teacher_remove_course_non_existing(self):
        teacher = Teacher("David", "Miller", "T55555")
        
        teacher.add_course("MATH101")
        teacher.add_course("PHY101")
        
        # Remove non-existing course - should not raise error
        teacher.remove_course("NONEXISTENT")
        self.assertEqual(len(teacher.courses), 2)  # No change
    
    def test_teacher_remove_course_empty_list(self):
        teacher = Teacher("Eve", "Taylor", "T66666")
        
        # Remove from empty course list - should not raise error
        teacher.remove_course("ANY_COURSE")
        self.assertEqual(len(teacher.courses), 0)
    
    def test_teacher_remove_multiple_courses(self):
        teacher = Teacher("Frank", "Anderson", "T77777")
        
        courses = ["ART101", "ART102", "ART201", "ART202"]
        for course in courses:
            teacher.add_course(course)
        
        teacher.remove_course("ART102")
        teacher.remove_course("ART202")
        
        self.assertEqual(len(teacher.courses), 2)
        self.assertEqual(teacher.courses, ["ART101", "ART201"])
    
    def test_teacher_profile(self):
        teacher = Teacher("Grace", "Lee", "T88888", "grace.lee@university.edu")
        
        # Create mock courses with code attribute
        class MockCourse:
            def __init__(self, code):
                self.code = code
        
        courses = [MockCourse("CS101"), MockCourse("CS201"), MockCourse("MATH101")]
        for course in courses:
            teacher.add_course(course)
        
        profile = teacher.profile()
        
        expected_profile = {
            "name": "Grace Lee",
            "id": "T88888",
            "courses": ["CS101", "CS201", "MATH101"]
        }
        self.assertEqual(profile, expected_profile)
    
    def test_teacher_profile_no_courses(self):
        teacher = Teacher("Henry", "Clark", "T99999")
        
        profile = teacher.profile()
        
        expected_profile = {
            "name": "Henry Clark",
            "id": "T99999",
            "courses": []
        }
        self.assertEqual(profile, expected_profile)
    
    def test_teacher_profile_with_courses_without_code(self):
        teacher = Teacher("Ivy", "Harris", "T00000")
        
        # Add courses without code attribute
        class CourseWithoutCode:
            def __init__(self, title):
                self.title = title
        
        course1 = CourseWithoutCode("Physics")
        course2 = "StringCourse"  # String course
        
        teacher.add_course(course1)
        teacher.add_course(course2)
        
        # This will cause AttributeError when trying to access course.code
        # But the provided code doesn't handle this case
        # We'll test what happens with the current implementation
        profile = teacher.profile()
        
        
    def test_teacher_office_assignment(self):
        teacher = Teacher("Jack", "White", "T12121")
        office = Office("Main Building", "Room 301", "+1112223333")
        
        teacher.office = office
        
        self.assertEqual(teacher.office, office)
        self.assertEqual(teacher.office.building, "Main Building")
        self.assertEqual(teacher.office.location(), "Main Building Room 301")
    
    def test_teacher_qualifications_management(self):
        teacher = Teacher("Karen", "Moore", "T13131")
        
        qualifications = [
            Qualification("PhD in Physics", "Caltech", 2010),
            Qualification("MSc in Education", "Harvard", 2005),
            Qualification("BSc in Mathematics", "MIT", 2000)
        ]
        
        # Add qualifications to teacher's list
        teacher.qualifications.extend(qualifications)
        
        self.assertEqual(len(teacher.qualifications), 3)
        self.assertEqual(teacher.qualifications[0].title, "PhD in Physics")
        self.assertEqual(teacher.qualifications[1].short(), "MSc in Education (2005)")
        self.assertEqual(teacher.qualifications[2].institution, "MIT")


class TestTeacherIntegration(unittest.TestCase):
    def test_complete_teacher_profile(self):
        # Create a teacher
        teacher = Teacher("Dr. Sarah", "Johnson", "T50505", "sarah.johnson@university.edu")
        
        # Create and assign office
        office = Office("Science Complex", "SC-408", "+1555123456")
        teacher.office = office
        
        # Add qualifications
        qualifications = [
            Qualification("PhD in Computer Science", "Stanford", 2015),
            Qualification("MSc in Artificial Intelligence", "MIT", 2010),
            Qualification("BSc in Software Engineering", "Berkeley", 2005)
        ]
        teacher.qualifications.extend(qualifications)
        
        # Create and add courses
        class Course:
            def __init__(self, code, title):
                self.code = code
                self.title = title
        
        courses = [
            Course("CS501", "Advanced Algorithms"),
            Course("CS502", "Machine Learning"),
            Course("CS503", "Data Science")
        ]
        for course in courses:
            teacher.add_course(course)
        
        # Verify complete profile
        profile = teacher.profile()
        expected_profile = {
            "name": "Dr. Sarah Johnson",
            "id": "T50505",
            "courses": ["CS501", "CS502", "CS503"]
        }
        self.assertEqual(profile, expected_profile)
        
        # Verify office
        self.assertEqual(teacher.office.location(), "Science Complex SC-408")
        self.assertEqual(teacher.office.phone, "+1555123456")
        
        # Verify qualifications
        self.assertEqual(len(teacher.qualifications), 3)
        self.assertEqual(teacher.qualifications[0].short(), "PhD in Computer Science (2015)")
        self.assertEqual(teacher.qualifications[1].institution, "MIT")
        
        # Verify inherited Person methods
        self.assertEqual(teacher.full_name(), "Dr. Sarah Johnson")
        
        contact_card = teacher.contact_card()
        expected_contact = {
            "name": "Dr. Sarah Johnson",
            "email": "sarah.johnson@university.edu",
            "phone": ""
        }
        self.assertEqual(contact_card, expected_contact)
    
    def test_teacher_course_management_workflow(self):
        teacher = Teacher("Prof. Michael", "Chen", "T60606")
        
        # Add multiple courses
        courses_to_add = ["MATH101", "MATH202", "MATH303", "MATH404"]
        for course in courses_to_add:
            teacher.add_course(course)
        
        self.assertEqual(len(teacher.courses), 4)
        
        # Remove some courses
        teacher.remove_course("MATH202")
        teacher.remove_course("MATH404")
        
        self.assertEqual(len(teacher.courses), 2)
        self.assertEqual(teacher.courses, ["MATH101", "MATH303"])
        
        # Add new courses
        teacher.add_course("MATH505")
        teacher.add_course("MATH606")
        
        self.assertEqual(len(teacher.courses), 4)
        self.assertEqual(teacher.courses, ["MATH101", "MATH303", "MATH505", "MATH606"])

class TestRequirement(unittest.TestCase):
    def test_requirement_initialization(self):
        req = Requirement("Complete all courses", 120)
        self.assertEqual(req.desc, "Complete all courses")
        self.assertEqual(req.credits, 120)

class TestGradeScale(unittest.TestCase):
    def test_initialization(self):
        scale = GradeScale({"A": 90, "B": 80})
        self.assertEqual(scale.mapping, {"A": 90, "B": 80})

    def test_grade_to_letter(self):
        scale = GradeScale({})
        self.assertEqual(scale.grade_to_letter(95), "A")
        self.assertEqual(scale.grade_to_letter(90), "A")
        self.assertEqual(scale.grade_to_letter(85), "B")
        self.assertEqual(scale.grade_to_letter(80), "B")

class TestDegree(unittest.TestCase):
    def test_degree_initialization(self):
        degree = Degree("Computer Science", "Bachelor")
        self.assertEqual(degree.name, "Computer Science")
        self.assertEqual(degree.level, "Bachelor")
        self.assertEqual(degree.requirements, [])

    def test_add_requirement(self):
        degree = Degree("Computer Science", "Bachelor")
        req = Requirement("Complete core courses", 60)
        degree.add_requirement(req)
        self.assertEqual(len(degree.requirements), 1)
        self.assertEqual(degree.requirements[0].desc, "Complete core courses")
        self.assertEqual(degree.requirements[0].credits, 60)

class TestProgram(unittest.TestCase):
    def test_program_initialization(self):
        program = Program("CS101", "Intro to Programming")
        self.assertEqual(program.code, "CS101")
        self.assertEqual(program.title, "Intro to Programming")
        self.assertEqual(program.courses, [])

    def test_add_course(self):
        program = Program("CS101", "Intro to Programming")
        course = Program("CS102", "Data Structures")
        program.add_course(course)
        self.assertEqual(len(program.courses), 1)
        self.assertEqual(program.courses[0].code, "CS102")

class TestExam(unittest.TestCase):
    def test_exam_initialization(self):
        course = Program("CS101", "Intro to Programming")
        exam = Exam(course, "2024-06-01")
        self.assertEqual(exam.course, course)
        self.assertEqual(exam.date, "2024-06-01")

    def test_schedule(self):
        course = Program("CS101", "Intro to Programming")
        exam = Exam(course, "2024-06-01")
        self.assertEqual(exam.schedule(), "Exam for CS101 on 2024-06-01")
        
class TestBadge(unittest.TestCase):
    def test_badge_initialization(self):
        badge = Badge("Python Expert", 3)
        self.assertEqual(badge.name, "Python Expert")
        self.assertEqual(badge.level, 3)
    
    def test_badge_default_level(self):
        badge = Badge("Beginner")
        self.assertEqual(badge.name, "Beginner")
        self.assertEqual(badge.level, 1)
    
    def test_badge_promote(self):
        badge = Badge("Contributor", 2)
        badge.promote()
        self.assertEqual(badge.level, 3)
        
        # Test multiple promotions
        badge.promote()
        badge.promote()
        self.assertEqual(badge.level, 5)


class TestEvent(unittest.TestCase):
    def test_event_initialization(self):
        event = Event("Tech Conference", "2024-07-15", "Convention Center")
        self.assertEqual(event.title, "Tech Conference")
        self.assertEqual(event.date, "2024-07-15")
        self.assertEqual(event.location, "Convention Center")
    
    def test_event_default_location(self):
        event = Event("Workshop", "2024-08-20")
        self.assertEqual(event.title, "Workshop")
        self.assertEqual(event.date, "2024-08-20")
        self.assertEqual(event.location, "")
    
    def test_event_describe(self):
        event = Event("Graduation", "2024-06-10", "Main Auditorium")
        description = event.describe()
        expected = "Graduation at Main Auditorium on 2024-06-10"
        self.assertEqual(description, expected)
        
        # Test with empty location
        event2 = Event("Meeting", "2024-05-01")
        description2 = event2.describe()
        expected2 = "Meeting at  on 2024-05-01"
        self.assertEqual(description2, expected2)


class TestNotification(unittest.TestCase):
    def test_notification_initialization(self):
        user = "student@example.com"
        notification = Notification(user, "Welcome", "Welcome to our platform!")
        self.assertEqual(notification.to, user)
        self.assertEqual(notification.subject, "Welcome")
        self.assertEqual(notification.body, "Welcome to our platform!")
        self.assertFalse(notification.sent)
    
    def test_notification_send(self):
        user = "teacher@example.com"
        notification = Notification(user, "Reminder", "Don't forget the meeting")
        
        # Initially not sent
        self.assertFalse(notification.sent)
        
        # Send notification
        notification.send()
        
        # Should be marked as sent
        self.assertTrue(notification.sent)
        
        # Send again (should remain sent)
        notification.send()
        self.assertTrue(notification.sent)


class TestRecoveryToken(unittest.TestCase):
    def test_recovery_token_initialization(self):
        user = "user123"
        token = RecoveryToken(user, "abc123token")
        self.assertEqual(token.user, user)
        self.assertEqual(token.token, "abc123token")
        self.assertFalse(token.used)
    
    def test_recovery_token_use_first_time(self):
        user = "user456"
        token = RecoveryToken(user, "xyz789token")
        
        # First use should succeed
        result = token.use()
        self.assertTrue(result)
        self.assertTrue(token.used)
    
    def test_recovery_token_reuse(self):
        user = "user789"
        token = RecoveryToken(user, "def456token")
        
        # First use
        result1 = token.use()
        self.assertTrue(result1)
        self.assertTrue(token.used)
        
        # Second use should fail
        result2 = token.use()
        self.assertFalse(result2)
        self.assertTrue(token.used)


class TestRolePerm(unittest.TestCase):
    def test_role_perm_initialization(self):
        perms = ["read", "write", "delete"]
        role_perm = RolePerm("admin", perms)
        self.assertEqual(role_perm.role, "admin")
        self.assertEqual(role_perm.perms, perms)
    
    def test_role_perm_has_existing_permission(self):
        perms = ["create", "edit", "publish"]
        role_perm = RolePerm("editor", perms)
        
        # Test existing permissions
        self.assertTrue(role_perm.has("create"))
        self.assertTrue(role_perm.has("edit"))
        self.assertTrue(role_perm.has("publish"))
    
    def test_role_perm_has_missing_permission(self):
        perms = ["view", "comment"]
        role_perm = RolePerm("viewer", perms)
        
        self.assertFalse(role_perm.has("edit"))
        self.assertFalse(role_perm.has("delete"))
        self.assertFalse(role_perm.has(""))


class TestCourse(unittest.TestCase):
    def test_course_initialization(self):
        course = Course("CS101", "Introduction to Programming", 4)
        self.assertEqual(course.code, "CS101")
        self.assertEqual(course.title, "Introduction to Programming")
        self.assertEqual(course.credits, 4)
        self.assertEqual(course.modules, [])
        self.assertIsNone(course.syllabus)
        self.assertEqual(course.schedule_options, [])
    
    def test_course_default_credits(self):
        course = Course("MATH101", "Calculus I")
        self.assertEqual(course.code, "MATH101")
        self.assertEqual(course.title, "Calculus I")
        self.assertEqual(course.credits, 3)  # default value
    
    def test_course_add_module(self):
        course = Course("PHY101", "Physics I", 4)
        module = Module("Mechanics", 12)
        
        course.add_module(module)
        
        self.assertEqual(len(course.modules), 1)
        self.assertEqual(course.modules[0].name, "Mechanics")
        self.assertEqual(course.modules[0].lessons, 12)
    
    def test_course_add_multiple_modules(self):
        course = Course("CHEM101", "Chemistry", 3)
        module1 = Module("Organic Chemistry", 8)
        module2 = Module("Inorganic Chemistry", 10)
        
        course.add_module(module1)
        course.add_module(module2)
        
        self.assertEqual(len(course.modules), 2)
        self.assertEqual(course.modules[0].name, "Organic Chemistry")
        self.assertEqual(course.modules[1].name, "Inorganic Chemistry")
    
    def test_course_available_times(self):
        course = Course("ENG101", "English Composition", 3)
        
        # Test with no schedule options
        self.assertEqual(course.available_times(), [])
        
        # Test with schedule options (mock the describe method)
        class MockTimeslot:
            def __init__(self, description):
                self.description = description
            def describe(self):
                return self.description
        
        timeslot1 = MockTimeslot("Mon 9:00-10:30")
        timeslot2 = MockTimeslot("Wed 14:00-15:30")
        course.schedule_options = [timeslot1, timeslot2]
        
        available_times = course.available_times()
        self.assertEqual(available_times, ["Mon 9:00-10:30", "Wed 14:00-15:30"])


class TestModule(unittest.TestCase):
    def test_module_initialization(self):
        module = Module("Data Structures", 15)
        self.assertEqual(module.name, "Data Structures")
        self.assertEqual(module.lessons, 15)
    
    def test_module_default_lessons(self):
        module = Module("Algorithms")
        self.assertEqual(module.name, "Algorithms")
        self.assertEqual(module.lessons, 10)  # default value
    
    def test_module_workload(self):
        # Test with custom lessons
        module1 = Module("Advanced Topics", 20)
        self.assertEqual(module1.workload(), 40)  # 20 * 2
        
        # Test with default lessons
        module2 = Module("Basics")
        self.assertEqual(module2.workload(), 20)  # 10 * 2
        
        # Test with zero lessons
        module3 = Module("Introduction", 0)
        self.assertEqual(module3.workload(), 0)  # 0 * 2


class TestSyllabus(unittest.TestCase):
    def test_syllabus_initialization(self):
        topics = ["Variables", "Loops", "Functions", "Classes"]
        syllabus = Syllabus("Programming fundamentals", topics)
        self.assertEqual(syllabus.summary, "Programming fundamentals")
        self.assertEqual(syllabus.topics, topics)
    
    def test_syllabus_topic_count(self):
        # Test with multiple topics
        topics1 = ["Intro", "Data Types", "Control Structures", "OOP"]
        syllabus1 = Syllabus("Java Programming", topics1)
        self.assertEqual(syllabus1.topic_count(), 4)
        
        # Test with empty topics
        syllabus2 = Syllabus("Empty Course", [])
        self.assertEqual(syllabus2.topic_count(), 0)
        
        # Test with single topic
        syllabus3 = Syllabus("Special Topic", ["Advanced Concepts"])
        self.assertEqual(syllabus3.topic_count(), 1)


class TestCourseSchedule(unittest.TestCase):
    def test_course_schedule_initialization(self):
        course = Course("MATH202", "Linear Algebra", 3)
        schedule = CourseSchedule(course, "Mon/Wed 10:00-11:30")
        
        self.assertEqual(schedule.course, course)
        self.assertEqual(schedule.timeslot, "Mon/Wed 10:00-11:30")
    
    def test_course_schedule_is_conflict(self):
        course1 = Course("CS101", "Programming", 4)
        course2 = Course("MATH101", "Calculus", 4)
        
        schedule1 = CourseSchedule(course1, "Mon 9:00-10:30")
        schedule2 = CourseSchedule(course2, "Mon 9:00-10:30")  # Same timeslot
        schedule3 = CourseSchedule(course2, "Tue 11:00-12:30")  # Different timeslot
        
        # Test conflict with same timeslot
        self.assertTrue(schedule1.is_conflict(schedule2))
        self.assertTrue(schedule2.is_conflict(schedule1))
        
        # Test no conflict with different timeslot
        self.assertFalse(schedule1.is_conflict(schedule3))
        self.assertFalse(schedule3.is_conflict(schedule1))
        
        # Test with different types of timeslot representations
        schedule4 = CourseSchedule(course1, "Room A")
        schedule5 = CourseSchedule(course2, "Room A")
        schedule6 = CourseSchedule(course2, "Room B")
        
        self.assertTrue(schedule4.is_conflict(schedule5))
        self.assertFalse(schedule4.is_conflict(schedule6))


class TestIntegration(unittest.TestCase):
    def test_course_with_module_and_syllabus(self):
        # Create a complete course with modules and syllabus
        course = Course("CS301", "Software Engineering", 4)
        
        # Add modules
        module1 = Module("Requirements Analysis", 8)
        module2 = Module("Software Design", 10)
        module3 = Module("Testing", 6)
        
        course.add_module(module1)
        course.add_module(module2)
        course.add_module(module3)
        
        # Set syllabus
        topics = [
            "Software Development Lifecycle",
            "Agile Methodology", 
            "Version Control",
            "Testing Strategies",
            "Deployment"
        ]
        syllabus = Syllabus("Comprehensive guide to software engineering practices", topics)
        course.syllabus = syllabus
        
        # Verify everything is connected correctly
        self.assertEqual(course.code, "CS301")
        self.assertEqual(len(course.modules), 3)
        self.assertEqual(course.modules[0].name, "Requirements Analysis")
        self.assertEqual(course.modules[1].workload(), 20)  # 10 * 2
        self.assertEqual(course.syllabus.topic_count(), 5)
        self.assertEqual(course.syllabus.topics[0], "Software Development Lifecycle")


class TestAccount(unittest.TestCase):
    def test_account_initialization(self):
        account = Account("John Doe", 1000.0)
        self.assertEqual(account.owner, "John Doe")
        self.assertEqual(account.balance, 1000.0)
        self.assertEqual(account.transactions, [])
    
    def test_account_default_balance(self):
        account = Account("Jane Smith")
        self.assertEqual(account.owner, "Jane Smith")
        self.assertEqual(account.balance, 0.0)
        self.assertEqual(account.transactions, [])
    
    def test_account_deposit(self):
        account = Account("Bob", 500.0)
        new_balance = account.deposit(200.0)
        
        self.assertEqual(new_balance, 700.0)
        self.assertEqual(account.balance, 700.0)
        self.assertEqual(len(account.transactions), 1)
        self.assertEqual(account.transactions[0], ("deposit", 200.0))
    
    def test_account_multiple_deposits(self):
        account = Account("Alice", 100.0)
        account.deposit(50.0)
        account.deposit(25.0)
        
        self.assertEqual(account.balance, 175.0)
        self.assertEqual(len(account.transactions), 2)
        self.assertEqual(account.transactions[0], ("deposit", 50.0))
        self.assertEqual(account.transactions[1], ("deposit", 25.0))
    
    def test_account_withdraw_success(self):
        account = Account("Charlie", 300.0)
        new_balance = account.withdraw(150.0)
        
        self.assertEqual(new_balance, 150.0)
        self.assertEqual(account.balance, 150.0)
        self.assertEqual(len(account.transactions), 1)
        self.assertEqual(account.transactions[0], ("withdraw", 150.0))
    
    def test_account_withdraw_insufficient_funds(self):
        account = Account("David", 100.0)
        
        with self.assertRaises(Exception) as context:
            account.withdraw(200.0)
        
        self.assertEqual(str(context.exception), "insufficient")
        self.assertEqual(account.balance, 100.0)  # Balance unchanged
        self.assertEqual(len(account.transactions), 0)  # No transaction recorded
    
    def test_account_transaction_history(self):
        account = Account("Eve", 1000.0)
        account.deposit(500.0)
        account.withdraw(200.0)
        account.deposit(100.0)
        account.withdraw(50.0)
        
        self.assertEqual(account.balance, 1350.0)
        self.assertEqual(len(account.transactions), 4)
        expected_transactions = [
            ("deposit", 500.0),
            ("withdraw", 200.0),
            ("deposit", 100.0),
            ("withdraw", 50.0)
        ]
        self.assertEqual(account.transactions, expected_transactions)


class TestBilling(unittest.TestCase):
    def test_billing_initialization(self):
        billing = Billing()
        self.assertEqual(billing.invoices, [])
    
    def test_billing_create_invoice(self):
        billing = Billing()
        
        # Create first invoice
        invoice_id1 = billing.create_invoice("Student1", 500.0)
        self.assertEqual(invoice_id1, 0)
        self.assertEqual(len(billing.invoices), 1)
        self.assertEqual(billing.invoices[0], ("Student1", 500.0))
        
        # Create second invoice
        invoice_id2 = billing.create_invoice("Student2", 750.0)
        self.assertEqual(invoice_id2, 1)
        self.assertEqual(len(billing.invoices), 2)
        self.assertEqual(billing.invoices[0], ("Student1", 500.0))
        self.assertEqual(billing.invoices[1], ("Student2", 750.0))
    
    def test_billing_multiple_invoices_same_owner(self):
        billing = Billing()
        
        billing.create_invoice("SameStudent", 100.0)
        billing.create_invoice("SameStudent", 200.0)
        billing.create_invoice("SameStudent", 300.0)
        
        self.assertEqual(len(billing.invoices), 3)
        self.assertEqual(billing.invoices[0], ("SameStudent", 100.0))
        self.assertEqual(billing.invoices[1], ("SameStudent", 200.0))
        self.assertEqual(billing.invoices[2], ("SameStudent", 300.0))


class TestCard(unittest.TestCase):
    def test_card_initialization(self):
        account = Account("Card Owner", 1000.0)
        card = Card(account, "1234-5678-9012-3456", "CARD OWNER")
        
        self.assertEqual(card.account, account)
        self.assertEqual(card.card_number, "1234-5678-9012-3456")
        self.assertEqual(card.holder_name, "CARD OWNER")
        self.assertFalse(card.blocked)
    
    def test_card_block(self):
        account = Account("Test User", 500.0)
        card = Card(account, "1111-2222-3333-4444", "TEST USER")
        
        self.assertFalse(card.blocked)
        card.block()
        self.assertTrue(card.blocked)
    
    def test_card_unblock(self):
        account = Account("Test User", 500.0)
        card = Card(account, "1111-2222-3333-4444", "TEST USER")
        
        card.block()
        self.assertTrue(card.blocked)
        
        card.unblock()
        self.assertFalse(card.blocked)
    
    def test_card_block_unblock_cycle(self):
        account = Account("Cycle User", 300.0)
        card = Card(account, "5555-6666-7777-8888", "CYCLE USER")
        
        # Multiple block/unblock operations
        card.block()
        card.block()  # Should remain blocked
        self.assertTrue(card.blocked)
        
        card.unblock()
        card.unblock()  # Should remain unblocked
        self.assertFalse(card.blocked)
        
        card.block()
        self.assertTrue(card.blocked)


class TestScholarship(unittest.TestCase):
    def test_scholarship_initialization(self):
        student = "Student123"
        scholarship = Scholarship(student, 5000.0, "Academic Excellence")
        
        self.assertEqual(scholarship.awardee, student)
        self.assertEqual(scholarship.amount, 5000.0)
        self.assertEqual(scholarship.reason, "Academic Excellence")
    
    def test_scholarship_default_reason(self):
        student = "Student456"
        scholarship = Scholarship(student, 3000.0)
        
        self.assertEqual(scholarship.awardee, student)
        self.assertEqual(scholarship.amount, 3000.0)
        self.assertEqual(scholarship.reason, "")
    
    def test_scholarship_award_success(self):
        # Create a student with an account
        class Student:
            def __init__(self):
                self.account = Account("StudentWithAccount", 100.0)
        
        student = Student()
        scholarship = Scholarship(student, 1500.0, "Merit-based")
        
        result = scholarship.award()
        
        self.assertTrue(result)
        self.assertEqual(student.account.balance, 1600.0)  # 100 + 1500
    
    def test_scholarship_award_failure(self):
        # Create a student without an account
        class StudentWithoutAccount:
            pass
        
        student = StudentWithoutAccount()
        scholarship = Scholarship(student, 2000.0, "Need-based")
        
        result = scholarship.award()
        
        self.assertFalse(result)
        # No change expected since award failed


class TestTransaction(unittest.TestCase):
    def test_transaction_initialization(self):
        from_account = Account("Sender", 1000.0)
        to_account = Account("Receiver", 500.0)
        from_card = Card(from_account, "1111-1111-1111-1111", "SENDER")
        to_card = Card(to_account, "2222-2222-2222-2222", "RECEIVER")
        
        transaction = Transaction(from_card, to_card, 300.0, "Tuition payment")
        
        self.assertEqual(transaction.from_card, from_card)
        self.assertEqual(transaction.to_card, to_card)
        self.assertEqual(transaction.amount, 300.0)
        self.assertEqual(transaction.reference, "Tuition payment")
    
    def test_transaction_default_reference(self):
        from_account = Account("Sender", 1000.0)
        to_account = Account("Receiver", 500.0)
        from_card = Card(from_account, "1111-1111-1111-1111", "SENDER")
        to_card = Card(to_account, "2222-2222-2222-2222", "RECEIVER")
        
        transaction = Transaction(from_card, to_card, 100.0)
        
        self.assertEqual(transaction.reference, "")
    
    def test_transaction_execute_success(self):
        from_account = Account("Sender", 1000.0)
        to_account = Account("Receiver", 500.0)
        from_card = Card(from_account, "1111-1111-1111-1111", "SENDER")
        to_card = Card(to_account, "2222-2222-2222-2222", "RECEIVER")
        
        transaction = Transaction(from_card, to_card, 300.0, "Transfer")
        
        result = transaction.execute()
        
        self.assertTrue(result)
        self.assertEqual(from_account.balance, 700.0)  # 1000 - 300
        self.assertEqual(to_account.balance, 800.0)   # 500 + 300
        
        # Check transaction history
        self.assertEqual(len(from_account.transactions), 1)
        self.assertEqual(from_account.transactions[0], ("withdraw", 300.0))
        
        self.assertEqual(len(to_account.transactions), 1)
        self.assertEqual(to_account.transactions[0], ("deposit", 300.0))
    
    def test_transaction_execute_blocked_from_card(self):
        from_account = Account("Sender", 1000.0)
        to_account = Account("Receiver", 500.0)
        from_card = Card(from_account, "1111-1111-1111-1111", "SENDER")
        to_card = Card(to_account, "2222-2222-2222-2222", "RECEIVER")
        
        from_card.block()  # Block the sender's card
        
        transaction = Transaction(from_card, to_card, 200.0)
        
        result = transaction.execute()
        
        self.assertFalse(result)
        self.assertEqual(from_account.balance, 1000.0)  # No change
        self.assertEqual(to_account.balance, 500.0)    # No change
    
    def test_transaction_execute_blocked_to_card(self):
        from_account = Account("Sender", 1000.0)
        to_account = Account("Receiver", 500.0)
        from_card = Card(from_account, "1111-1111-1111-1111", "SENDER")
        to_card = Card(to_account, "2222-2222-2222-2222", "RECEIVER")
        
        to_card.block()  # Block the receiver's card
        
        transaction = Transaction(from_card, to_card, 200.0)
        
        result = transaction.execute()
        
        self.assertFalse(result)
        self.assertEqual(from_account.balance, 1000.0)  # No change
        self.assertEqual(to_account.balance, 500.0)    # No change
    
    def test_transaction_execute_insufficient_funds(self):
        from_account = Account("Sender", 100.0)
        to_account = Account("Receiver", 500.0)
        from_card = Card(from_account, "1111-1111-1111-1111", "SENDER")
        to_card = Card(to_account, "2222-2222-2222-2222", "RECEIVER")
        
        transaction = Transaction(from_card, to_card, 200.0)  # More than sender has
        
        with self.assertRaises(Exception) as context:
            transaction.execute()
        
        self.assertEqual(str(context.exception), "insufficient funds")
        self.assertEqual(from_account.balance, 100.0)  # No change
        self.assertEqual(to_account.balance, 500.0)    # No change


class TestFinancialIntegration(unittest.TestCase):
    def test_complete_financial_flow(self):
        # Create accounts
        student_account = Account("Student", 100.0)
        university_account = Account("University", 50000.0)
        
        # Create cards
        student_card = Card(student_account, "1234-1234-1234-1234", "STUDENT")
        university_card = Card(university_account, "9999-9999-9999-9999", "UNIVERSITY")
        
        # Create billing for tuition
        billing = Billing()
        tuition_invoice_id = billing.create_invoice("Student", 5000.0)
        
        # Student gets scholarship
        class Student:
            def __init__(self, account):
                self.account = account
        
        student_obj = Student(student_account)
        scholarship = Scholarship(student_obj, 6000.0, "Merit Scholarship")
        scholarship.award()
        
        # Verify scholarship deposited
        self.assertEqual(student_account.balance, 6100.0)  # 100 + 6000
        
        # Student pays tuition
        tuition_payment = Transaction(student_card, university_card, 5000.0, "Tuition Payment")
        result = tuition_payment.execute()
        
        self.assertTrue(result)
        self.assertEqual(student_account.balance, 1100.0)  # 6100 - 5000
        self.assertEqual(university_account.balance, 55000.0)  # 50000 + 5000

class TestRoom(unittest.TestCase):
    def test_room_initialization(self):
        room = Room("101", 1)
        self.assertEqual(room.number, "101")
        self.assertEqual(room.floor, 1)
        self.assertFalse(room.occupied)
        self.assertFalse(hasattr(room, 'resident'))
    
    def test_room_initialization_occupied(self):
        room = Room("202", 2, True)
        self.assertEqual(room.number, "202")
        self.assertEqual(room.floor, 2)
        self.assertTrue(room.occupied)
    
    def test_room_assign_success(self):
        room = Room("101", 1, False)
        resident = "John Doe"
        
        result = room.assign(resident)
        
        self.assertTrue(result)
        self.assertTrue(room.occupied)
        self.assertEqual(room.resident, resident)
    
    def test_room_assign_failure_already_occupied(self):
        room = Room("202", 2, True)
        room.resident = "Existing Resident"
        new_resident = "New Resident"
        
        result = room.assign(new_resident)
        
        self.assertFalse(result)
        self.assertTrue(room.occupied)
        self.assertEqual(room.resident, "Existing Resident")  # Resident unchanged
    
    def test_room_assign_multiple_attempts(self):
        room = Room("303", 3, False)
        resident1 = "First Applicant"
        
        # First assignment should succeed
        result1 = room.assign(resident1)
        self.assertTrue(result1)
        self.assertTrue(room.occupied)
        self.assertEqual(room.resident, resident1)
        
        # Second assignment should fail
        resident2 = "Second Applicant"
        result2 = room.assign(resident2)
        self.assertFalse(result2)
        self.assertEqual(room.resident, resident1)  # Still first resident


class TestDorm(unittest.TestCase):
    def test_dorm_initialization(self):
        dorm = Dorm("North Hall")
        self.assertEqual(dorm.name, "North Hall")
        self.assertEqual(dorm.capacity, 100)
        self.assertEqual(dorm.rooms, [])
    
    def test_dorm_initialization_with_capacity(self):
        dorm = Dorm("South Hall", 150)
        self.assertEqual(dorm.name, "South Hall")
        self.assertEqual(dorm.capacity, 150)
        self.assertEqual(dorm.rooms, [])
    
    def test_dorm_vacancy_empty(self):
        dorm = Dorm("East Hall", 50)
        self.assertEqual(dorm.vacancy(), 50)  # No rooms, so full capacity available
    
    def test_dorm_vacancy_with_rooms(self):
        dorm = Dorm("West Hall", 100)
        
        # Add some rooms
        room1 = Room("101", 1, False)
        room2 = Room("102", 1, True)
        room3 = Room("201", 2, False)
        room4 = Room("202", 2, True)
        room5 = Room("301", 3, True)
        
        dorm.rooms = [room1, room2, room3, room4, room5]
        
        # 3 occupied rooms out of 5, capacity 100, so vacancy = 100 - 3 = 97
        self.assertEqual(dorm.vacancy(), 97)
    
    def test_dorm_vacancy_all_occupied(self):
        dorm = Dorm("Central Hall", 75)
        
        # Add only occupied rooms
        room1 = Room("101", 1, True)
        room2 = Room("102", 1, True)
        
        dorm.rooms = [room1, room2]
        
        self.assertEqual(dorm.vacancy(), 73)  # 75 - 2 = 73
    
    def test_dorm_vacancy_all_vacant(self):
        dorm = Dorm("Park Hall", 200)
        
        # Add only vacant rooms
        room1 = Room("101", 1, False)
        room2 = Room("102", 1, False)
        room3 = Room("201", 2, False)
        
        dorm.rooms = [room1, room2, room3]
        
        self.assertEqual(dorm.vacancy(), 200)  # No occupied rooms
    
    def test_dorm_vacancy_mixed_room_states(self):
        dorm = Dorm("Mixed Hall", 50)
        
        # Create rooms with various states
        rooms = []
        for i in range(10):
            room = Room(f"10{i}", 1, i % 2 == 0)  # Even indexes are occupied
            rooms.append(room)
        
        dorm.rooms = rooms
        
        # 5 occupied rooms (indexes 0, 2, 4, 6, 8)
        self.assertEqual(dorm.vacancy(), 45)  # 50 - 5 = 45


class TestLease(unittest.TestCase):
    def test_lease_initialization(self):
        room = Room("101", 1, False)
        resident = "John Doe"
        lease = Lease(resident, room, "2024-01-01", "2024-12-31")
        
        self.assertEqual(lease.resident, resident)
        self.assertEqual(lease.room, room)
        self.assertEqual(lease.start_date, "2024-01-01")
        self.assertEqual(lease.end_date, "2024-12-31")
    
    def test_lease_is_active_always_true(self):
        room = Room("202", 2, True)
        resident = "Jane Smith"
        lease = Lease(resident, room, "2024-01-01", "2024-12-31")
        
        # Test with various dates
        self.assertTrue(lease.is_active("2024-01-01"))
        self.assertTrue(lease.is_active("2024-06-15"))
        self.assertTrue(lease.is_active("2024-12-31"))
        self.assertTrue(lease.is_active("2023-12-31"))  # Before start date
        self.assertTrue(lease.is_active("2025-01-01"))  # After end date
        self.assertTrue(lease.is_active(""))  # Empty string
        self.assertTrue(lease.is_active("invalid-date"))  # Invalid format


class TestMaintenanceRequest(unittest.TestCase):
    def test_maintenance_request_initialization(self):
        room = Room("101", 1, True)
        request = MaintenanceRequest(room, "Leaky faucet")
        
        self.assertEqual(request.room, room)
        self.assertEqual(request.issue, "Leaky faucet")
        self.assertEqual(request.status, "open")
    
    def test_maintenance_request_resolve(self):
        room = Room("202", 2, True)
        request = MaintenanceRequest(room, "Broken window")
        
        # Initially open
        self.assertEqual(request.status, "open")
        
        # Resolve the request
        request.resolve()
        
        # Should be closed
        self.assertEqual(request.status, "closed")
        
        # Resolve again (should remain closed)
        request.resolve()
        self.assertEqual(request.status, "closed")
    
    def test_maintenance_request_different_issues(self):
        room = Room("303", 3, True)
        
        issues = [
            "No hot water",
            "Electrical outlet not working", 
            "Heating system failure",
            "Pest infestation",
            "Broken furniture"
        ]
        
        for issue in issues:
            request = MaintenanceRequest(room, issue)
            self.assertEqual(request.issue, issue)
            self.assertEqual(request.status, "open")
            
            request.resolve()
            self.assertEqual(request.status, "closed")


class TestHousingIntegration(unittest.TestCase):
    def test_complete_housing_workflow(self):
        # Create a dorm
        dorm = Dorm("University Hall", 200)
        
        # Create and add rooms to dorm
        rooms = [
            Room("101", 1, False),
            Room("102", 1, False), 
            Room("201", 2, False),
            Room("202", 2, False),
            Room("301", 3, False)
        ]
        dorm.rooms = rooms
        
        # Initially all rooms vacant
        self.assertEqual(dorm.vacancy(), 200)
        
        # Assign residents to some rooms
        residents = ["Alice", "Bob", "Charlie"]
        for i, resident in enumerate(residents):
            success = rooms[i].assign(resident)
            self.assertTrue(success)
        
        # Check vacancy after assignments
        self.assertEqual(dorm.vacancy(), 197)  # 200 - 3 = 197
        
        # Create leases for the residents
        leases = []
        for i, resident in enumerate(residents):
            lease = Lease(resident, rooms[i], "2024-09-01", "2025-05-31")
            leases.append(lease)
            self.assertTrue(lease.is_active("2024-10-15"))
        
        # Create maintenance requests
        requests = []
        issues = ["Broken bed", "No heating", "Clogged drain"]
        for i, issue in enumerate(issues):
            request = MaintenanceRequest(rooms[i], issue)
            requests.append(request)
            self.assertEqual(request.status, "open")
        
        # Resolve some maintenance requests
        requests[0].resolve()
        requests[2].resolve()
        
        self.assertEqual(requests[0].status, "closed")
        self.assertEqual(requests[1].status, "open")  # This one wasn't resolved
        self.assertEqual(requests[2].status, "closed")
        
        # Try to assign to an already occupied room
        new_resident = "David"
        success = rooms[0].assign(new_resident)
        self.assertFalse(success)
        self.assertEqual(rooms[0].resident, "Alice")  # Original resident remains
    
    def test_edge_cases(self):
        # Test with empty room list
        dorm = Dorm("Empty Hall", 100)
        self.assertEqual(dorm.vacancy(), 100)
        
        # Test with room that has no resident attribute when vacant
        room = Room("999", 9, False)
        self.assertFalse(hasattr(room, 'resident'))
        
        # Assign resident
        room.assign("New Resident")
        self.assertTrue(hasattr(room, 'resident'))
        self.assertEqual(room.resident, "New Resident")
        
        # Test maintenance request with empty issue
        request = MaintenanceRequest(room, "")
        self.assertEqual(request.issue, "")
        request.resolve()
        self.assertEqual(request.status, "closed")


class TestAuthor(unittest.TestCase):
    def test_author_initialization(self):
        author = Author("J.K. Rowling", "1965-07-31")
        self.assertEqual(author.name, "J.K. Rowling")
        self.assertEqual(author.born, "1965-07-31")
    
    def test_author_initialization_default_born(self):
        author = Author("George Orwell")
        self.assertEqual(author.name, "George Orwell")
        self.assertEqual(author.born, "")
    
    def test_author_profile(self):
        author = Author("Isaac Asimov", "1920-01-02")
        profile = author.profile()
        
        expected_profile = {
            "name": "Isaac Asimov",
            "born": "1920-01-02"
        }
        self.assertEqual(profile, expected_profile)
    
    def test_author_profile_default_born(self):
        author = Author("Unknown Author")
        profile = author.profile()
        
        expected_profile = {
            "name": "Unknown Author",
            "born": ""
        }
        self.assertEqual(profile, expected_profile)
    
    def test_author_empty_name(self):
        author = Author("", "1900-01-01")
        self.assertEqual(author.name, "")
        self.assertEqual(author.born, "1900-01-01")
        
        profile = author.profile()
        expected_profile = {"name": "", "born": "1900-01-01"}
        self.assertEqual(profile, expected_profile)


class TestBook(unittest.TestCase):
    def test_book_initialization(self):
        author = Author("J.R.R. Tolkien", "1892-01-03")
        book = Book("The Hobbit", author, "978-0547928227")
        
        self.assertEqual(book.title, "The Hobbit")
        self.assertEqual(book.author, author)
        self.assertEqual(book.isbn, "978-0547928227")
        self.assertTrue(book.available)
    
    def test_book_checkout_success(self):
        author = Author("Agatha Christie", "1890-09-15")
        book = Book("Murder on the Orient Express", author, "978-0062693662")
        
        # Initially available
        self.assertTrue(book.available)
        
        # Checkout should succeed
        borrower = "Alice"
        result = book.checkout(borrower)
        
        self.assertTrue(result)
        self.assertFalse(book.available)
    
    def test_book_checkout_failure_already_checked_out(self):
        author = Author("Stephen King", "1947-09-21")
        book = Book("The Shining", author, "978-0307743657")
        
        # First checkout succeeds
        book.checkout("Bob")
        self.assertFalse(book.available)
        
        # Second checkout should fail
        result = book.checkout("Charlie")
        self.assertFalse(result)
        self.assertFalse(book.available)  # Still unavailable
    
    def test_book_multiple_checkout_attempts(self):
        author = Author("Jane Austen", "1775-12-16")
        book = Book("Pride and Prejudice", author, "978-0141439518")
        
        borrowers = ["David", "Eve", "Frank"]
        results = []
        
        for borrower in borrowers:
            results.append(book.checkout(borrower))
        
        # Only first checkout should succeed
        self.assertTrue(results[0])
        self.assertFalse(results[1])
        self.assertFalse(results[2])
        self.assertFalse(book.available)
    
    def test_book_checkout_with_different_borrower_types(self):
        author = Author("Mark Twain", "1835-11-30")
        book = Book("Adventures of Huckleberry Finn", author, "978-0486280615")
        
        # Test with string borrower
        result1 = book.checkout("Student123")
        self.assertTrue(result1)
        
        # Reset book availability for next test
        book.available = True
        
        # Test with numeric borrower
        result2 = book.checkout(12345)
        self.assertTrue(result2)
        
        # Reset book availability for next test
        book.available = True
        
        # Test with object borrower
        class Borrower:
            def __init__(self, name):
                self.name = name
        
        borrower_obj = Borrower("Faculty Member")
        result3 = book.checkout(borrower_obj)
        self.assertTrue(result3)


class TestBorrowRecord(unittest.TestCase):
    def test_borrow_record_initialization(self):
        author = Author("Harper Lee", "1926-04-28")
        book = Book("To Kill a Mockingbird", author, "978-0061120084")
        borrower = "Student456"
        
        record = BorrowRecord(book, borrower, "2024-12-31")
        
        self.assertEqual(record.book, book)
        self.assertEqual(record.borrower, borrower)
        self.assertEqual(record.due_date, "2024-12-31")
    
    def test_borrow_record_is_overdue_always_false(self):
        author = Author("F. Scott Fitzgerald", "1896-09-24")
        book = Book("The Great Gatsby", author, "978-0743273565")
        
        record = BorrowRecord(book, "Faculty789", "2024-06-15")
        
        # Test with various dates - should always return False
        test_dates = [
            "2024-01-01",  # Before due date
            "2024-06-15",  # On due date
            "2024-12-31",  # After due date
            "invalid-date",  # Invalid format
            "",  # Empty string
            "2023-12-31",  # Way before due date
            "2025-01-01"   # Way after due date
        ]
        
        for date in test_dates:
            self.assertFalse(record.is_overdue(date))
    
    def test_borrow_record_different_borrower_types(self):
        author = Author("Leo Tolstoy", "1828-09-09")
        book = Book("War and Peace", author, "978-0140447934")
        
        # Test with different borrower types
        borrowers = [
            "String Borrower",
            12345,
            {"id": "user123", "name": "Object Borrower"}
        ]
        
        for borrower in borrowers:
            record = BorrowRecord(book, borrower, "2024-12-31")
            self.assertEqual(record.borrower, borrower)
            self.assertFalse(record.is_overdue("2024-12-31"))


class TestLibrary(unittest.TestCase):
    def test_library_initialization(self):
        library = Library("Central Library", "123 Main St")
        
        self.assertEqual(library.name, "Central Library")
        self.assertEqual(library.address, "123 Main St")
        self.assertEqual(library.catalog, [])
        self.assertEqual(library.borrow_records, [])
    
    def test_library_add_book(self):
        library = Library("City Library", "456 Oak Ave")
        author = Author("Ernest Hemingway", "1899-07-21")
        book = Book("The Old Man and the Sea", author, "978-0684801223")
        
        library.add_book(book)
        
        self.assertEqual(len(library.catalog), 1)
        self.assertEqual(library.catalog[0], book)
    
    def test_library_add_multiple_books(self):
        library = Library("University Library", "789 Campus Dr")
        
        authors_books = [
            (Author("Virginia Woolf", "1882-01-25"), "Mrs. Dalloway", "978-0156628709"),
            (Author("James Joyce", "1882-02-02"), "Ulysses", "978-0394743127"),
            (Author("Marcel Proust", "1871-07-10"), "In Search of Lost Time", "978-0142437964")
        ]
        
        for author, title, isbn in authors_books:
            book = Book(title, author, isbn)
            library.add_book(book)
        
        self.assertEqual(len(library.catalog), 3)
        self.assertEqual(library.catalog[0].title, "Mrs. Dalloway")
        self.assertEqual(library.catalog[1].author.name, "James Joyce")
        self.assertEqual(library.catalog[2].isbn, "978-0142437964")
    
    def test_library_find_book_exact_match(self):
        library = Library("Search Test Library", "999 Test St")
        
        books = [
            Book("The Catcher in the Rye", Author("J.D. Salinger"), "978-0316769174"),
            Book("Cat's Cradle", Author("Kurt Vonnegut"), "978-0385333481"),
            Book("The Great Catsby", Author("Fake Author"), "978-0000000000"),  # Similar title
            Book("1984", Author("George Orwell"), "978-0451524935")
        ]
        
        for book in books:
            library.add_book(book)
        
        # Search for "Cat" - should find 3 books
        results = library.find_book("Cat")
        self.assertEqual(len(results), 3)
        
        # Verify the specific books found
        titles_found = [book.title for book in results]
        expected_titles = ["The Catcher in the Rye", "Cat's Cradle", "The Great Catsby"]
        self.assertEqual(set(titles_found), set(expected_titles))
    
    def test_library_find_book_case_insensitive(self):
        library = Library("Case Test Library", "111 Case Ave")
        
        library.add_book(Book("HARRY POTTER", Author("J.K. Rowling"), "978-0439708180"))
        library.add_book(Book("harry potter and the chamber", Author("J.K. Rowling"), "978-0439064873"))
        library.add_book(Book("The HaRrY Potter Phenomenon", Author("Critic"), "978-1234567890"))
        library.add_book(Book("Lord of the Rings", Author("J.R.R. Tolkien"), "978-0544003415"))
        
        # Search with different cases
        results1 = library.find_book("HARRY")
        results2 = library.find_book("harry")
        results3 = library.find_book("Harry")
        
        self.assertEqual(len(results1), 3)
        self.assertEqual(len(results2), 3)
        self.assertEqual(len(results3), 3)
    
    def test_library_find_book_no_matches(self):
        library = Library("Empty Search Library", "222 NoMatch Rd")
        
        library.add_book(Book("Moby Dick", Author("Herman Melville"), "978-0142437247"))
        library.add_book(Book("Don Quixote", Author("Miguel de Cervantes"), "978-0060934347"))
        
        results = library.find_book("Shakespeare")
        self.assertEqual(len(results), 0)
        self.assertEqual(results, [])
    
    def test_library_find_book_empty_string(self):
        library = Library("Empty String Library", "333 Empty St")
        
        library.add_book(Book("Book One", Author("Author One"), "111"))
        library.add_book(Book("Book Two", Author("Author Two"), "222"))
        
        # Empty string should match all books (since "" is in every string)
        results = library.find_book("")
        self.assertEqual(len(results), 2)
    
    def test_library_find_book_partial_title(self):
        library = Library("Partial Match Library", "444 Partial Rd")
        
        library.add_book(Book("The Wonderful Wizard of Oz", Author("L. Frank Baum"), "978-0140621679"))
        library.add_book(Book("Wizard's First Rule", Author("Terry Goodkind"), "978-0812548051"))
        library.add_book(Book("Harry Potter and the Sorcerer's Stone", Author("J.K. Rowling"), "978-0439708180"))
        
        results = library.find_book("Wizard")
        self.assertEqual(len(results), 2)
        
        titles_found = [book.title for book in results]
        expected_titles = ["The Wonderful Wizard of Oz", "Wizard's First Rule"]
        self.assertEqual(set(titles_found), set(expected_titles))


class TestLibraryIntegration(unittest.TestCase):
    def test_complete_library_workflow(self):
        # Create library
        library = Library("Community Library", "123 Learning Lane")
        
        # Create authors
        authors = [
            Author("Douglas Adams", "1952-03-11"),
            Author("Neil Gaiman", "1960-11-10"),
            Author("Terry Pratchett", "1948-04-28")
        ]
        
        # Create books
        books = [
            Book("The Hitchhiker's Guide to the Galaxy", authors[0], "978-0345391803"),
            Book("American Gods", authors[1], "978-0062059888"),
            Book("Good Omens", authors[2], "978-0060853983"),
            Book("Neverwhere", authors[1], "978-0060557812")
        ]
        
        # Add books to library
        for book in books:
            library.add_book(book)
        
        # Verify catalog
        self.assertEqual(len(library.catalog), 4)
        
        # Search for books by Gaiman
        gaiman_books = library.find_book("Gaiman")
        self.assertEqual(len(gaiman_books), 0)  # Search is by title, not author
        
        gaiman_titles = library.find_book("Gods")  # Search by title
        self.assertEqual(len(gaiman_titles), 1)
        self.assertEqual(gaiman_titles[0].title, "American Gods")
        
        # Checkout a book
        borrower = "Library Member 001"
        checkout_result = books[0].checkout(borrower)
        self.assertTrue(checkout_result)
        self.assertFalse(books[0].available)
        
        # Create borrow record
        record = BorrowRecord(books[0], borrower, "2024-12-31")
        library.borrow_records.append(record)
        
        self.assertEqual(len(library.borrow_records), 1)
        self.assertFalse(record.is_overdue("2024-12-31"))
        
        # Try to checkout the same book again
        second_checkout = books[0].checkout("Another Borrower")
        self.assertFalse(second_checkout)
        
        # Checkout a different book
        another_borrower = "Library Member 002"
        checkout_result2 = books[1].checkout(another_borrower)
        self.assertTrue(checkout_result2)
        
        # Search for available books
        all_books = library.find_book("")  # Empty string returns all books
        available_books = [book for book in all_books if book.available]
        self.assertEqual(len(available_books), 2)  # 2 out of 4 books still available


class TestAddress(unittest.TestCase):
    def test_address_initialization(self):
        address = Address("123 Main St", "Springfield", "12345", "USA")
        self.assertEqual(address.street, "123 Main St")
        self.assertEqual(address.city, "Springfield")
        self.assertEqual(address.zip_code, "12345")
        self.assertEqual(address.country, "USA")
    
    def test_address_formatted(self):
        address = Address("456 Oak Avenue", "Metropolis", "67890", "United States")
        formatted = address.formatted()
        expected = "456 Oak Avenue, Metropolis, 67890, United States"
        self.assertEqual(formatted, expected)
    
    def test_address_formatted_empty_fields(self):
        # Test with empty strings
        address = Address("", "", "", "")
        formatted = address.formatted()
        expected = ", , , "
        self.assertEqual(formatted, expected)
    
    def test_address_formatted_partial_empty(self):
        address = Address("789 Pine Rd", "", "54321", "Canada")
        formatted = address.formatted()
        expected = "789 Pine Rd, , 54321, Canada"
        self.assertEqual(formatted, expected)
    
    def test_address_formatted_special_characters(self):
        address = Address("St. Patrick's Street", "Dublin", "D02 VH98", "Ireland")
        formatted = address.formatted()
        expected = "St. Patrick's Street, Dublin, D02 VH98, Ireland"
        self.assertEqual(formatted, expected)


class TestContactInfo(unittest.TestCase):
    def test_contact_info_initialization(self):
        contact = ContactInfo("john@example.com", "+1234567890")
        self.assertEqual(contact.email, "john@example.com")
        self.assertEqual(contact.phone, "+1234567890")
        self.assertEqual(contact.alt_phone, "")
    
    def test_contact_info_initialization_with_alt_phone(self):
        contact = ContactInfo("jane@example.com", "+0987654321", "+1112223333")
        self.assertEqual(contact.email, "jane@example.com")
        self.assertEqual(contact.phone, "+0987654321")
        self.assertEqual(contact.alt_phone, "+1112223333")
    
    def test_contact_info_reachable_with_email_and_phone(self):
        contact = ContactInfo("test@example.com", "+1234567890")
        self.assertTrue(contact.reachable())
    
    def test_contact_info_reachable_with_email_only(self):
        contact = ContactInfo("test@example.com", "")
        self.assertTrue(contact.reachable())
    
    def test_contact_info_reachable_with_phone_only(self):
        contact = ContactInfo("", "+1234567890")
        self.assertTrue(contact.reachable())
    
    def test_contact_info_reachable_with_alt_phone_only(self):
        contact = ContactInfo("", "", "+1234567890")
        # Note: reachable() only checks email and phone, not alt_phone
        self.assertFalse(contact.reachable())
    
    def test_contact_info_not_reachable(self):
        contact = ContactInfo("", "")
        self.assertFalse(contact.reachable())
    
    def test_contact_info_reachable_with_whitespace(self):
        # Test with whitespace-only strings (should be considered empty for boolean check)
        contact = ContactInfo("   ", "   ")
        self.assertTrue(contact.reachable())
    
    def test_contact_info_edge_cases(self):
        # Test with very long strings
        long_email = "a" * 100 + "@example.com"
        long_phone = "+1" + "0" * 20
        contact = ContactInfo(long_email, long_phone)
        self.assertTrue(contact.reachable())


class TestIDCard(unittest.TestCase):
    def test_id_card_initialization(self):
        id_card = IDCard("A123456789", "University", "2025-12-31")
        self.assertEqual(id_card.uid, "A123456789")
        self.assertEqual(id_card.issued_by, "University")
        self.assertEqual(id_card.valid_until, "2025-12-31")
    
    def test_id_card_is_valid_always_true(self):
        id_card = IDCard("B987654321", "Government", "2024-06-30")
        
        # Test with various dates - should always return True
        test_dates = [
            "2023-01-01",  # Before valid_until
            "2024-06-30",  # On valid_until
            "2025-01-01",  # After valid_until
            "invalid-date",  # Invalid format
            "",  # Empty string
            "2020-01-01",  # Way before
            "2030-01-01"   # Way after
        ]
        
        for date in test_dates:
            self.assertTrue(id_card.is_valid(date))
    
    def test_id_card_special_uid_formats(self):
        test_cases = [
            ("123-456-789", "DMV", "2026-01-01"),
            ("", "Test Issuer", "2024-12-31"),  # Empty UID
            ("X" * 50, "Long Issuer", "2025-06-15")  # Very long UID
        ]
        
        for uid, issuer, valid_until in test_cases:
            id_card = IDCard(uid, issuer, valid_until)
            self.assertEqual(id_card.uid, uid)
            self.assertEqual(id_card.issued_by, issuer)
            self.assertEqual(id_card.valid_until, valid_until)
            self.assertTrue(id_card.is_valid("2024-01-01"))


class TestPerson(unittest.TestCase):
    def test_person_initialization(self):
        person = Person("John", "Doe", "john.doe@example.com", "+1234567890")
        self.assertEqual(person.first_name, "John")
        self.assertEqual(person.last_name, "Doe")
        self.assertEqual(person.email, "john.doe@example.com")
        self.assertEqual(person.phone, "+1234567890")
        self.assertIsNone(person.metadata)
    
    def test_person_initialization_minimal(self):
        person = Person("Jane", "Smith")
        self.assertEqual(person.first_name, "Jane")
        self.assertEqual(person.last_name, "Smith")
        self.assertEqual(person.email, "")
        self.assertEqual(person.phone, "")
        self.assertIsNone(person.metadata)
    
    def test_person_initialization_with_metadata(self):
        metadata = {"department": "Engineering", "role": "Developer"}
        person = Person("Bob", "Johnson", "bob@example.com", "+0987654321", metadata)
        self.assertEqual(person.first_name, "Bob")
        self.assertEqual(person.last_name, "Johnson")
        self.assertEqual(person.email, "bob@example.com")
        self.assertEqual(person.phone, "+0987654321")
        self.assertEqual(person.metadata, metadata)
    
    def test_person_full_name(self):
        person = Person("Alice", "Brown")
        full_name = person.full_name()
        self.assertEqual(full_name, "Alice Brown")
    
    def test_person_full_name_empty(self):
        person = Person("", "")
        full_name = person.full_name()
        self.assertEqual(full_name, " ")
    
    def test_person_full_name_special_characters(self):
        person = Person("José", "Muñoz")
        full_name = person.full_name()
        self.assertEqual(full_name, "José Muñoz")
    
    def test_person_contact_card(self):
        person = Person("John", "Doe", "john.doe@example.com", "+1234567890")
        contact_card = person.contact_card()
        
        expected = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890"
        }
        self.assertEqual(contact_card, expected)
    
    def test_person_contact_card_empty_contact(self):
        person = Person("Jane", "Smith")
        contact_card = person.contact_card()
        
        expected = {
            "name": "Jane Smith",
            "email": "",
            "phone": ""
        }
        self.assertEqual(contact_card, expected)
    
    def test_person_contact_card_partial_contact(self):
        person = Person("Bob", "Johnson", "bob@example.com")
        contact_card = person.contact_card()
        
        expected = {
            "name": "Bob Johnson",
            "email": "bob@example.com",
            "phone": ""
        }
        self.assertEqual(contact_card, expected)
    
    def test_person_contact_card_with_metadata_does_not_affect(self):
        metadata = {"notes": "VIP Client"}
        person = Person("Sarah", "Wilson", "sarah@example.com", "+1112223333", metadata)
        contact_card = person.contact_card()
        
        # Metadata should not appear in contact card
        expected = {
            "name": "Sarah Wilson",
            "email": "sarah@example.com",
            "phone": "+1112223333"
        }
        self.assertEqual(contact_card, expected)
        # But metadata should still be stored in person
        self.assertEqual(person.metadata, metadata)


class TestPersonalInfoIntegration(unittest.TestCase):
    def test_complete_personal_profile(self):
        # Create a person
        person = Person(
            "Michael", 
            "Chen", 
            "michael.chen@university.edu", 
            "+1-555-0123"
        )
        
        # Create address
        address = Address(
            "123 University Boulevard", 
            "College Town", 
            "12345", 
            "United States"
        )
        
        # Create contact info
        contact_info = ContactInfo(
            person.email, 
            person.phone, 
            "+1-555-0456"
        )
        
        # Create ID card
        id_card = IDCard(
            "STU-789012", 
            "University of Testing", 
            "2025-08-31"
        )
        
        # Verify all components work together
        self.assertEqual(person.full_name(), "Michael Chen")
        
        contact_card = person.contact_card()
        expected_contact = {
            "name": "Michael Chen",
            "email": "michael.chen@university.edu",
            "phone": "+1-555-0123"
        }
        self.assertEqual(contact_card, expected_contact)
        
        self.assertEqual(address.formatted(), "123 University Boulevard, College Town, 12345, United States")
        self.assertTrue(contact_info.reachable())
        self.assertTrue(id_card.is_valid("2024-01-15"))
    
    def test_edge_cases_and_boundary_conditions(self):
        # Test with very long names
        long_first_name = "A" * 100
        long_last_name = "B" * 100
        person = Person(long_first_name, long_last_name)
        self.assertEqual(person.full_name(), f"{long_first_name} {long_last_name}")
        
        # Test with special characters in all fields
        special_person = Person("John-O'Brian", "Déjàvu", "email+tag@example.com", "+1 (555) 123-4567")
        special_address = Address("St. Mary's Street #123", "San José", "12345-6789", "Côte d'Ivoire")
        
        self.assertEqual(special_person.full_name(), "John-O'Brian Déjàvu")
        self.assertTrue("San José" in special_address.formatted())
        
        # Test empty objects
        empty_person = Person("", "")
        empty_contact = ContactInfo("", "")
        empty_id = IDCard("", "", "")
        
        self.assertEqual(empty_person.full_name(), " ")
        self.assertFalse(empty_contact.reachable())
        self.assertTrue(empty_id.is_valid(""))


class TestTimeSlot(unittest.TestCase):
    def test_time_slot_initialization(self):
        time_slot = TimeSlot("Monday", "09:00", "10:30", "Lecture")
        self.assertEqual(time_slot.day, "Monday")
        self.assertEqual(time_slot.start, "09:00")
        self.assertEqual(time_slot.end, "10:30")
        self.assertEqual(time_slot.label, "Lecture")
    
    def test_time_slot_initialization_default_label(self):
        time_slot = TimeSlot("Friday", "14:00", "15:30")
        self.assertEqual(time_slot.day, "Friday")
        self.assertEqual(time_slot.start, "14:00")
        self.assertEqual(time_slot.end, "15:30")
        self.assertEqual(time_slot.label, "")
    
    def test_time_slot_describe(self):
        time_slot = TimeSlot("Wednesday", "10:00", "11:30", "Lab Session")
        description = time_slot.describe()
        expected = "Wednesday 10:00-11:30 Lab Session"
        self.assertEqual(description, expected)
    
    def test_time_slot_describe_empty_label(self):
        time_slot = TimeSlot("Thursday", "13:00", "14:30")
        description = time_slot.describe()
        expected = "Thursday 13:00-14:30 "
        self.assertEqual(description, expected)
    
    def test_time_slot_describe_special_times(self):
        test_cases = [
            ("Monday", "00:00", "23:59", "All Day"),
            ("Sunday", "12:00", "12:00", "No Duration"),
            ("Tuesday", "09:00 AM", "10:30 AM", "Morning")
        ]
        
        for day, start, end, label in test_cases:
            time_slot = TimeSlot(day, start, end, label)
            description = time_slot.describe()
            expected = f"{day} {start}-{end} {label}"
            self.assertEqual(description, expected)
    
    def test_time_slot_edge_cases(self):
        # Empty strings
        time_slot = TimeSlot("", "", "", "")
        self.assertEqual(time_slot.describe(), " -  ")
        
        # Very long label
        long_label = "A" * 100
        time_slot = TimeSlot("Day", "00:00", "24:00", long_label)
        self.assertEqual(time_slot.label, long_label)


class TestCalendarEntry(unittest.TestCase):
    def test_calendar_entry_initialization(self):
        time_slot = TimeSlot("Monday", "09:00", "10:30", "Meeting")
        entry = CalendarEntry("John Doe", time_slot, "Conference Room A")
        
        self.assertEqual(entry.owner, "John Doe")
        self.assertEqual(entry.timeslot, time_slot)
        self.assertEqual(entry.location, "Conference Room A")
    
    def test_calendar_entry_initialization_default_location(self):
        time_slot = TimeSlot("Tuesday", "14:00", "15:00", "Study")
        entry = CalendarEntry("Jane Smith", time_slot)
        
        self.assertEqual(entry.owner, "Jane Smith")
        self.assertEqual(entry.timeslot, time_slot)
        self.assertEqual(entry.location, "")
    
    def test_calendar_entry_conflicts_with_same_day_and_start(self):
        time_slot1 = TimeSlot("Monday", "10:00", "11:00", "Class")
        time_slot2 = TimeSlot("Monday", "10:00", "12:00", "Meeting")  # Same day and start
        
        entry1 = CalendarEntry("Student A", time_slot1, "Room 101")
        entry2 = CalendarEntry("Student B", time_slot2, "Room 102")
        
        self.assertTrue(entry1.conflicts_with(entry2))
        self.assertTrue(entry2.conflicts_with(entry1))
    
    def test_calendar_entry_conflicts_with_different_day(self):
        time_slot1 = TimeSlot("Monday", "10:00", "11:00", "Class")
        time_slot2 = TimeSlot("Tuesday", "10:00", "11:00", "Class")  # Different day
        
        entry1 = CalendarEntry("Student A", time_slot1, "Room 101")
        entry2 = CalendarEntry("Student A", time_slot2, "Room 101")
        
        self.assertFalse(entry1.conflicts_with(entry2))
        self.assertFalse(entry2.conflicts_with(entry1))
    
    def test_calendar_entry_conflicts_with_different_start_time(self):
        time_slot1 = TimeSlot("Wednesday", "09:00", "10:00", "Lecture")
        time_slot2 = TimeSlot("Wednesday", "10:00", "11:00", "Tutorial")  # Different start
        
        entry1 = CalendarEntry("Professor X", time_slot1, "Auditorium")
        entry2 = CalendarEntry("Professor X", time_slot2, "Lab")
        
        self.assertFalse(entry1.conflicts_with(entry2))
        self.assertFalse(entry2.conflicts_with(entry1))
    
    def test_calendar_entry_conflicts_with_same_day_different_cases(self):
        # Test case sensitivity in day comparison
        time_slot1 = TimeSlot("monday", "09:00", "10:00", "Lowercase")
        time_slot2 = TimeSlot("Monday", "09:00", "10:00", "Capitalized")  # Different case
        
        entry1 = CalendarEntry("User1", time_slot1)
        entry2 = CalendarEntry("User2", time_slot2)
        
        # Since comparison is exact string match, these should conflict
        self.assertTrue(entry1.conflicts_with(entry2))
    
    def test_calendar_entry_conflicts_with_same_start_different_end(self):
        # Same day and start, different end times should still conflict
        time_slot1 = TimeSlot("Friday", "13:00", "14:00", "Short")
        time_slot2 = TimeSlot("Friday", "13:00", "15:00", "Long")  # Same start, different end
        
        entry1 = CalendarEntry("Person A", time_slot1)
        entry2 = CalendarEntry("Person B", time_slot2)
        
        self.assertTrue(entry1.conflicts_with(entry2))
    
    def test_calendar_entry_conflicts_with_self(self):
        time_slot = TimeSlot("Thursday", "11:00", "12:00", "Self Meeting")
        entry = CalendarEntry("Me", time_slot, "My Office")
        
        # Entry should conflict with itself
        self.assertTrue(entry.conflicts_with(entry))
    
    def test_calendar_entry_edge_cases(self):
        # Empty time slots
        empty_time_slot = TimeSlot("", "", "", "")
        entry = CalendarEntry("", empty_time_slot, "")
        
        self.assertEqual(entry.owner, "")
        self.assertEqual(entry.location, "")
        
        # Conflict check with empty entries
        entry1 = CalendarEntry("", TimeSlot("", "", ""), "")
        entry2 = CalendarEntry("", TimeSlot("", "", ""), "")
        
        self.assertTrue(entry1.conflicts_with(entry2))


class TestScheduler(unittest.TestCase):
    def test_scheduler_initialization(self):
        scheduler = Scheduler()
        self.assertEqual(scheduler.entries, [])
    
    def test_scheduler_add_entry(self):
        scheduler = Scheduler()
        time_slot = TimeSlot("Monday", "09:00", "10:00", "Added Entry")
        entry = CalendarEntry("Test User", time_slot, "Test Location")
        
        scheduler.add_entry(entry)
        
        self.assertEqual(len(scheduler.entries), 1)
        self.assertEqual(scheduler.entries[0], entry)
    
    def test_scheduler_add_multiple_entries(self):
        scheduler = Scheduler()
        
        entries = []
        for i in range(5):
            time_slot = TimeSlot(f"Day{i}", f"{i:02d}:00", f"{i+1:02d}:00", f"Entry {i}")
            entry = CalendarEntry(f"User{i}", time_slot, f"Location {i}")
            entries.append(entry)
            scheduler.add_entry(entry)
        
        self.assertEqual(len(scheduler.entries), 5)
        for i, entry in enumerate(entries):
            self.assertEqual(scheduler.entries[i], entry)
    
    def test_scheduler_find_entries_for_existing_owner(self):
        scheduler = Scheduler()
        
        # Add entries for different owners
        owners = ["Alice", "Bob", "Alice", "Charlie", "Alice"]
        for i, owner in enumerate(owners):
            time_slot = TimeSlot("Monday", f"{i:02d}:00", f"{i+1:02d}:00", f"Task {i}")
            entry = CalendarEntry(owner, time_slot, f"Room {i}")
            scheduler.add_entry(entry)
        
        # Find Alice's entries
        alice_entries = scheduler.find_entries_for("Alice")
        
        self.assertEqual(len(alice_entries), 3)
        for entry in alice_entries:
            self.assertEqual(entry.owner, "Alice")
    
    def test_scheduler_find_entries_for_non_existing_owner(self):
        scheduler = Scheduler()
        
        # Add some entries
        time_slot = TimeSlot("Tuesday", "10:00", "11:00", "Class")
        entry = CalendarEntry("Existing User", time_slot, "Somewhere")
        scheduler.add_entry(entry)
        
        # Search for non-existing owner
        non_existing_entries = scheduler.find_entries_for("Non Existing User")
        
        self.assertEqual(len(non_existing_entries), 0)
        self.assertEqual(non_existing_entries, [])
    
    def test_scheduler_find_entries_for_empty_scheduler(self):
        scheduler = Scheduler()
        
        entries = scheduler.find_entries_for("Any User")
        
        self.assertEqual(entries, [])
        self.assertEqual(len(entries), 0)
    
    def test_scheduler_find_entries_case_sensitive(self):
        scheduler = Scheduler()
        
        time_slot = TimeSlot("Wednesday", "14:00", "15:00", "Case Test")
        entry1 = CalendarEntry("alice", time_slot, "Room 1")  # lowercase
        entry2 = CalendarEntry("Alice", time_slot, "Room 2")  # capitalized
        
        scheduler.add_entry(entry1)
        scheduler.add_entry(entry2)
        
        # Search should be case-sensitive
        lowercase_results = scheduler.find_entries_for("alice")
        capitalized_results = scheduler.find_entries_for("Alice")
        
        self.assertEqual(len(lowercase_results), 1)
        self.assertEqual(lowercase_results[0].owner, "alice")
        
        self.assertEqual(len(capitalized_results), 1)
        self.assertEqual(capitalized_results[0].owner, "Alice")
    
    def test_scheduler_find_entries_with_objects_as_owners(self):
        scheduler = Scheduler()
        
        # Test with different object types as owners
        class User:
            def __init__(self, name):
                self.name = name
        
        user_obj = User("Object User")
        numeric_owner = 12345
        dict_owner = {"id": "user123"}
        
        time_slot = TimeSlot("Friday", "09:00", "10:00", "Object Test")
        
        entry1 = CalendarEntry(user_obj, time_slot, "Object Location")
        entry2 = CalendarEntry(numeric_owner, time_slot, "Numeric Location")
        entry3 = CalendarEntry(dict_owner, time_slot, "Dict Location")
        
        scheduler.add_entry(entry1)
        scheduler.add_entry(entry2)
        scheduler.add_entry(entry3)
        
        # Find entries for object owner
        user_entries = scheduler.find_entries_for(user_obj)
        self.assertEqual(len(user_entries), 1)
        self.assertEqual(user_entries[0].owner, user_obj)
        
        # Find entries for numeric owner
        numeric_entries = scheduler.find_entries_for(numeric_owner)
        self.assertEqual(len(numeric_entries), 1)
        self.assertEqual(numeric_entries[0].owner, numeric_owner)


class TestSchedulingIntegration(unittest.TestCase):
    def test_complete_scheduling_workflow(self):
        scheduler = Scheduler()
        
        # Create multiple time slots
        time_slots = [
            TimeSlot("Monday", "09:00", "10:30", "Math Lecture"),
            TimeSlot("Monday", "11:00", "12:30", "Physics Lab"),
            TimeSlot("Tuesday", "09:00", "10:30", "History Seminar"),
            TimeSlot("Wednesday", "14:00", "15:30", "Chemistry Tutorial"),
            TimeSlot("Monday", "09:00", "10:30", "Conflict Class")  # Same time as first
        ]
        
        # Create calendar entries
        entries = []
        for i, time_slot in enumerate(time_slots):
            owner = "Student" if i % 2 == 0 else "Professor"
            location = f"Building {i // 2 + 1}"
            entry = CalendarEntry(owner, time_slot, location)
            entries.append(entry)
            scheduler.add_entry(entry)
        
        # Verify all entries added
        self.assertEqual(len(scheduler.entries), 5)
        
        # Find entries for Student
        student_entries = scheduler.find_entries_for("Student")
        self.assertEqual(len(student_entries), 3)
        
        # Find entries for Professor
        professor_entries = scheduler.find_entries_for("Professor")
        self.assertEqual(len(professor_entries), 2)
        
        # Check for conflicts
        self.assertTrue(entries[0].conflicts_with(entries[4]))  # Same Monday 09:00
        self.assertFalse(entries[0].conflicts_with(entries[1]))  # Different times on Monday
        self.assertFalse(entries[1].conflicts_with(entries[2]))  # Different days
        
        # Verify time slot descriptions
        self.assertEqual(entries[0].timeslot.describe(), "Monday 09:00-10:30 Math Lecture")
        self.assertEqual(entries[3].timeslot.describe(), "Wednesday 14:00-15:30 Chemistry Tutorial")
    
    def test_edge_cases_integration(self):
        scheduler = Scheduler()
        
        # Test with empty and special values
        empty_time_slot = TimeSlot("", "", "", "")
        empty_entry = CalendarEntry("", empty_time_slot, "")
        
        scheduler.add_entry(empty_entry)
        
        # Find empty owner
        empty_owner_entries = scheduler.find_entries_for("")
        self.assertEqual(len(empty_owner_entries), 1)
        
        # Check conflict with empty entries
        another_empty_entry = CalendarEntry("", TimeSlot("", "", ""), "")
        self.assertTrue(empty_entry.conflicts_with(another_empty_entry))
        
        # Test description of empty time slot
        self.assertEqual(empty_entry.timeslot.describe(), " -  ")


class TestGradeRecord(unittest.TestCase):
    def test_grade_record_initialization(self):
        grade_record = GradeRecord("CS101", 85.5, 4)
        self.assertEqual(grade_record.course_code, "CS101")
        self.assertEqual(grade_record.grade, 85.5)
        self.assertEqual(grade_record.credits, 4)
    
    def test_grade_record_default_credits(self):
        grade_record = GradeRecord("MATH202", 92.0)
        self.assertEqual(grade_record.course_code, "MATH202")
        self.assertEqual(grade_record.grade, 92.0)
        self.assertEqual(grade_record.credits, 3)  # default value
    
    def test_grade_record_edge_cases(self):
        # Test with minimum grade
        min_grade = GradeRecord("PHY101", 0.0, 1)
        self.assertEqual(min_grade.grade, 0.0)
        
        # Test with maximum grade
        max_grade = GradeRecord("CHEM101", 100.0, 5)
        self.assertEqual(max_grade.grade, 100.0)
        
        # Test with decimal grade
        decimal_grade = GradeRecord("BIO101", 87.75, 3)
        self.assertEqual(decimal_grade.grade, 87.75)
        
        # Test with empty course code
        empty_code = GradeRecord("", 75.0, 2)
        self.assertEqual(empty_code.course_code, "")


class TestTranscript(unittest.TestCase):
    def test_transcript_initialization(self):
        transcript = Transcript()
        self.assertEqual(transcript.entries, [])
    
    def test_transcript_add_grade(self):
        transcript = Transcript()
        grade_record = GradeRecord("CS101", 85.0, 4)
        
        transcript.add_grade(grade_record)
        
        self.assertEqual(len(transcript.entries), 1)
        self.assertEqual(transcript.entries[0], grade_record)
    
    def test_transcript_add_multiple_grades(self):
        transcript = Transcript()
        
        grades = [
            GradeRecord("CS101", 85.0, 4),
            GradeRecord("MATH202", 92.0, 3),
            GradeRecord("PHY101", 78.5, 4)
        ]
        
        for grade in grades:
            transcript.add_grade(grade)
        
        self.assertEqual(len(transcript.entries), 3)
        self.assertEqual(transcript.entries[0].course_code, "CS101")
        self.assertEqual(transcript.entries[1].grade, 92.0)
        self.assertEqual(transcript.entries[2].credits, 4)
    
    def test_transcript_gpa_no_entries(self):
        transcript = Transcript()
        gpa = transcript.gpa()
        self.assertEqual(gpa, 0.0)
    
    def test_transcript_gpa_single_entry(self):
        transcript = Transcript()
        transcript.add_grade(GradeRecord("CS101", 85.0, 4))
        
        gpa = transcript.gpa()
        self.assertEqual(gpa, 85.0)
    
    def test_transcript_gpa_multiple_entries(self):
        transcript = Transcript()
        
        grades = [
            GradeRecord("CS101", 80.0, 4),
            GradeRecord("MATH202", 90.0, 3),
            GradeRecord("PHY101", 70.0, 4)
        ]
        
        for grade in grades:
            transcript.add_grade(grade)
        
        # GPA = (80 + 90 + 70) / 3 = 240 / 3 = 80.0
        gpa = transcript.gpa()
        self.assertEqual(gpa, 80.0)
    
    def test_transcript_gpa_with_zero_grades(self):
        transcript = Transcript()
        
        transcript.add_grade(GradeRecord("FAIL101", 0.0, 3))
        transcript.add_grade(GradeRecord("PASS101", 100.0, 3))
        
        gpa = transcript.gpa()
        self.assertEqual(gpa, 50.0)  # (0 + 100) / 2 = 50.0


class TestStudent(unittest.TestCase):
    def test_student_initialization(self):
        student = Student("John", "Doe", "S12345", "john.doe@university.edu")
        
        self.assertEqual(student.first_name, "John")
        self.assertEqual(student.last_name, "Doe")
        self.assertEqual(student.student_id, "S12345")
        self.assertEqual(student.email, "john.doe@university.edu")
        self.assertEqual(student.enrolled_courses, [])
        self.assertIsNone(student.transcript)
        self.assertIsNone(student.housing)
    
    def test_student_initialization_default_email(self):
        student = Student("Jane", "Smith", "S67890")
        
        self.assertEqual(student.first_name, "Jane")
        self.assertEqual(student.last_name, "Smith")
        self.assertEqual(student.student_id, "S67890")
        self.assertEqual(student.email, "")
        self.assertEqual(student.enrolled_courses, [])
    
    def test_student_enroll_course(self):
        student = Student("Alice", "Brown", "S11111")
        course = "CS101"
        
        student.enroll(course)
        
        self.assertEqual(len(student.enrolled_courses), 1)
        self.assertEqual(student.enrolled_courses[0], course)
    
    def test_student_enroll_multiple_courses(self):
        student = Student("Bob", "Johnson", "S22222")
        
        courses = ["CS101", "MATH202", "PHY101", "CHEM101"]
        
        for course in courses:
            student.enroll(course)
        
        self.assertEqual(len(student.enrolled_courses), 4)
        self.assertEqual(student.enrolled_courses, courses)


class TestEnrollmentRecord(unittest.TestCase):
    def test_enrollment_record_initialization(self):
        student = Student("John", "Doe", "S12345")
        course = "CS101"
        
        record = EnrollmentRecord(student, course, "active")
        
        self.assertEqual(record.student, student)
        self.assertEqual(record.course, course)
        self.assertEqual(record.status, "active")
    
    def test_enrollment_record_default_status(self):
        student = Student("Jane", "Smith", "S67890")
        course = "MATH202"
        
        record = EnrollmentRecord(student, course)
        
        self.assertEqual(record.student, student)
        self.assertEqual(record.course, course)
        self.assertEqual(record.status, "active")  # default value
    
    def test_enrollment_record_is_active(self):
        student = Student("Alice", "Brown", "S11111")
        
        # Active enrollment
        active_record = EnrollmentRecord(student, "CS101", "active")
        self.assertTrue(active_record.is_active())
        
        # Inactive enrollment
        inactive_record = EnrollmentRecord(student, "CS101", "inactive")
        self.assertFalse(inactive_record.is_active())
        
        # Other statuses
        other_statuses = ["completed", "dropped", "withdrawn", "pending"]
        for status in other_statuses:
            record = EnrollmentRecord(student, "CS101", status)
            self.assertFalse(record.is_active())
    
    def test_enrollment_record_different_course_types(self):
        student = Student("Bob", "Johnson", "S22222")
        
        # Test with string course
        string_course_record = EnrollmentRecord(student, "CS101")
        self.assertEqual(string_course_record.course, "CS101")
        
        # Test with object course
        class Course:
            def __init__(self, code, title):
                self.code = code
                self.title = title
        
        course_obj = Course("CS101", "Introduction to Programming")
        object_course_record = EnrollmentRecord(student, course_obj)
        self.assertEqual(object_course_record.course, course_obj)


class TestCalendarEntry(unittest.TestCase):
    def test_calendar_entry_initialization(self):
        time_slot = TimeSlot("Monday", "09:00", "10:30")
        entry = CalendarEntry("Student123", time_slot, "Room 101")
        
        self.assertEqual(entry.owner, "Student123")
        self.assertEqual(entry.timeslot, time_slot)
        self.assertEqual(entry.location, "Room 101")
        # Note: enrolled_courses is not initialized in the provided code
    
    def test_calendar_entry_default_location(self):
        time_slot = TimeSlot("Tuesday", "14:00", "15:30")
        entry = CalendarEntry("Professor456", time_slot)
        
        self.assertEqual(entry.owner, "Professor456")
        self.assertEqual(entry.timeslot, time_slot)
        self.assertEqual(entry.location, "")
    
    def test_calendar_entry_conflicts_with_same_time(self):
        time_slot1 = TimeSlot("Monday", "10:00", "11:00")
        time_slot2 = TimeSlot("Monday", "10:00", "12:00")  # Same day and start
        
        entry1 = CalendarEntry("Student1", time_slot1, "Room 101")
        entry2 = CalendarEntry("Student2", time_slot2, "Room 102")
        
        self.assertTrue(entry1.conflicts_with(entry2))
        self.assertTrue(entry2.conflicts_with(entry1))
    
    def test_calendar_entry_conflicts_with_different_time(self):
        time_slot1 = TimeSlot("Wednesday", "09:00", "10:00")
        time_slot2 = TimeSlot("Wednesday", "10:00", "11:00")  # Different start time
        
        entry1 = CalendarEntry("Student1", time_slot1, "Room 101")
        entry2 = CalendarEntry("Student1", time_slot2, "Room 101")
        
        self.assertFalse(entry1.conflicts_with(entry2))
        self.assertFalse(entry2.conflicts_with(entry1))
    
    def test_calendar_entry_conflicts_with_different_day(self):
        time_slot1 = TimeSlot("Monday", "10:00", "11:00")
        time_slot2 = TimeSlot("Tuesday", "10:00", "11:00")  # Different day
        
        entry1 = CalendarEntry("Student1", time_slot1, "Room 101")
        entry2 = CalendarEntry("Student1", time_slot2, "Room 101")
        
        self.assertFalse(entry1.conflicts_with(entry2))
        self.assertFalse(entry2.conflicts_with(entry1))
    
    def test_calendar_entry_enroll_and_drop(self):
        # Note: These methods seem out of place in CalendarEntry
        # but we'll test them as they appear in the provided code
        time_slot = TimeSlot("Friday", "13:00", "14:00")
        entry = CalendarEntry("Student123", time_slot, "Lab")
        
        # Manually initialize enrolled_courses since it's not in __init__
        entry.enrolled_courses = []
        
        course1 = "CS101"
        course2 = "MATH202"
        
        # Test enrolling courses
        result1 = entry.enroll(course1)
        self.assertTrue(result1)
        self.assertEqual(len(entry.enrolled_courses), 1)
        self.assertEqual(entry.enrolled_courses[0], course1)
        
        result2 = entry.enroll(course2)
        self.assertTrue(result2)
        self.assertEqual(len(entry.enrolled_courses), 2)
        self.assertEqual(entry.enrolled_courses[1], course2)
        
        # Test enrolling duplicate course
        result3 = entry.enroll(course1)
        self.assertFalse(result3)
        self.assertEqual(len(entry.enrolled_courses), 2)  # No change
        
        # Test dropping courses
        result4 = entry.drop(course1)
        self.assertTrue(result4)
        self.assertEqual(len(entry.enrolled_courses), 1)
        self.assertEqual(entry.enrolled_courses[0], course2)
        
        # Test dropping non-existent course
        result5 = entry.drop("NONEXISTENT")
        self.assertFalse(result5)
        self.assertEqual(len(entry.enrolled_courses), 1)  # No change


class TestStudentIntegration(unittest.TestCase):
    def test_complete_student_system(self):
        # Create a student
        student = Student("Emily", "Davis", "S99999", "emily.davis@university.edu")
        
        # Create a transcript
        transcript = Transcript()
        
        # Add grades to transcript
        grades = [
            GradeRecord("CS101", 88.0, 4),
            GradeRecord("MATH202", 92.5, 3),
            GradeRecord("PHY101", 79.0, 4)
        ]
        
        for grade in grades:
            transcript.add_grade(grade)
        
        # Assign transcript to student
        student.transcript = transcript
        
        # Enroll student in courses
        courses = ["CS201", "MATH303", "CHEM101"]
        for course in courses:
            student.enroll(course)
        
        # Create enrollment records
        enrollment_records = []
        for course in courses:
            record = EnrollmentRecord(student, course, "active")
            enrollment_records.append(record)
        
        # Create calendar entries for classes
        time_slots = [
            TimeSlot("Monday", "09:00", "10:30", "CS201 Lecture"),
            TimeSlot("Wednesday", "11:00", "12:30", "MATH303 Seminar"),
            TimeSlot("Friday", "14:00", "15:30", "CHEM101 Lab")
        ]
        
        calendar_entries = []
        for i, time_slot in enumerate(time_slots):
            entry = CalendarEntry(student.student_id, time_slot, f"Building {i+1}")
            calendar_entries.append(entry)
        
        # Verify everything is connected correctly
        self.assertEqual(student.full_name(), "Emily Davis")
        self.assertEqual(len(student.enrolled_courses), 3)
        self.assertEqual(student.transcript.gpa(), (88.0 + 92.5 + 79.0) / 3)
        
        # Check enrollment status
        for record in enrollment_records:
            self.assertTrue(record.is_active())
        
        # Check for schedule conflicts
        self.assertFalse(calendar_entries[0].conflicts_with(calendar_entries[1]))
        self.assertFalse(calendar_entries[1].conflicts_with(calendar_entries[2]))
    
    def test_student_with_complete_academic_record(self):
        # Create a high-achieving student
        student = Student("Michael", "Chen", "S88888", "michael.chen@university.edu")
        
        # Create and populate transcript
        transcript = Transcript()
        excellent_grades = [
            GradeRecord("ADV_MATH", 97.0, 4),
            GradeRecord("COMP_SCI", 95.0, 4),
            GradeRecord("PHYSICS", 96.0, 4),
            GradeRecord("CHEMISTRY", 94.0, 3)
        ]
        
        for grade in excellent_grades:
            transcript.add_grade(grade)
        
        student.transcript = transcript
        
        # Calculate GPA
        gpa = student.transcript.gpa()
        expected_gpa = (97.0 + 95.0 + 96.0 + 94.0) / 4
        self.assertEqual(gpa, expected_gpa)
        
        # Verify student info
        self.assertEqual(student.contact_card()["name"], "Michael Chen")
        self.assertEqual(student.contact_card()["email"], "michael.chen@university.edu")

if __name__ == '__main__':
    unittest.main()