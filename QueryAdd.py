"""
This module deals with all additions to our tables
including boilerplate
"""

from db_connection import Session
from pprint import pprint
from sqlalchemy import Time
from Section import Section
from Department import Department
from Course import Course
from Student import Student
from Major import Major
from Enrollment import Enrollment
from StudentMajor import StudentMajor

from QuerySelect import select_course, select_department, select_student, select_section, select_major
from SQLAlchemyUtilities import check_unique

def add_letter_grade_enrollment(student, section, min_satisfactory):
    # Ensure no existing enrollment for the student and section
    existing_enrollment = find_enrollment(student, section)
    if existing_enrollment:
        raise ValueError("Enrollment already exists for this student and section.")
    
    # Create new LetterGrade enrollment
    new_enrollment = LetterGrade(student, section, min_satisfactory)
    save_enrollment(new_enrollment)  # Assuming a function to save enrollment in the database or data structure

    return new_enrollment

def add_department(session: Session):
    """
    Prompt the user for the information for a new department and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_abbreviation: bool = False
    name: str = ''
    abbreviation: str = ''
    while not unique_abbreviation or not unique_name:
        name = input("Department full name--> ")
        abbreviation = input("Department abbreviation--> ")
        name_count: int = session.query(Department).filter(Department.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a department by that name.  Try again.")
        if unique_name:
            abbreviation_count = session.query(Department). \
                filter(Department.abbreviation == abbreviation).count()
            unique_abbreviation = abbreviation_count == 0
            if not unique_abbreviation:
                print("We already have a department with that abbreviation.  Try again.")
    new_department = Department(abbreviation, name)
    session.add(new_department)


def add_course(session: Session):
    """
    This demonstrates how to use the utilities in SQLAlchemy Utilities for checking
    all the uniqueness constraints of a table in one method call.  The user
    experience is tougher to customize using this technique, but the benefit is that
    new uniqueness constraints will be automatically added to the list to be checked,
    without any change to the add_course code.

    Prompt the user for the information for a new course and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this course?")
    department: Department = select_department(session)
    description: str = input('Please enter the course description-->')
    units: int = int(input('How many units for this course-->'))
    violation = True  # Flag that we still have to prompt for fresh values
    while violation:
        name = input("Course full name--> ")
        number = int(input("Course number--> "))
        course = Course(department, number, name, description, units)
        violated_constraints = check_unique(Session, course)
        if len(violated_constraints) > 0:
            print('The following uniqueness constraints were violated:')
            pprint(violated_constraints)
            print('Please try again.')
        else:
            violation = False
    session.add(course)


def add_section(session: Session):
    """
    Prompt the user for the information for a new section and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which course are you adding this section?")
    course = select_course(session)
    section_number = int(input("Enter the Section Number --> "))
    section_year = int(input("Enter the Section Year --> "))
    semester = input("Enter the Semester --> ")
    schedule = input("Enter Schedule --> ")
    start_time = Time(input("Enter Start Time (HH:MM:SS) --> "))
    violation = True  # Flag that we still have to prompt for fresh values
    while violation:
        building = input("Section Building --> ")
        room = int(input("Section Room --> "))
        instructor = input("Instructor --> ")
        section = Section(course, section_number, section_year, semester, schedule, start_time, building, room, instructor)
        violated_constraints = check_unique(Session, course)

        if len(violated_constraints) > 0:
            print('The following uniqueness constraints were violated:')
            pprint(violated_constraints)
            print('Please try again.')
        else:
            violation = False
    session.add(section)



def add_section_student(session: Session):
    """Enroll a student in a section
    AKA add a section to the student's list of enrolled sections
    """
    student: Student = select_student(session)
    section: Section = select_section(session)

    student_section_count: int = session.query(Enrollment).filter(
        # Cant be enrolled in same section twice
        # kinda shitty but using all the PKs not surrogate
        Enrollment.studentID == student.studentID,
        Enrollment.sectionYear== section.sectionYear,
        Enrollment.semester == section.semester,
        Enrollment.courseNumber == section.courseNumber,
        Enrollment.departmentAbbreviation==section.departmentAbbreviation
    ).count()

    unique_student_section: bool = student_section_count == 0
    while not unique_student_section:
        print("That student is already enrolled in that section. Try again.")
        section = select_section(session)
        student = select_student(session)
    student.add_enrollment(section)
    session.add(section)
    session.flush()
def add_section_student2(session: Session):
    """
    Enroll student in section. Uses prof code 
    """
    student: Student = select_student(session)
    section: Section = select_section(session)

    """If a student is not enrolled in any section of
    CECS 323 during the Fall of 2023, then we certainly
    know that they are not enrolled in the section of 
    CECS 323 that the user has selected. """
    is_enrolled = session.query(Enrollment).join(Section).filter(
        # Seeing if there is a match of student enrolled in section
        Enrollment.student == student,
        Section.sectionNumber == section.sectionNumber,
        Section.departmentAbbreviation == section.departmentabbreviation,
        Section.courseNumber == section.courseNumber,
        Section.sectionYear == section.sectionYear,
        Section.semester == section.semester
    ).count() > 0

    if is_enrolled:
        print("That student is already enrolled in that section. Try again.")
    student.add_enrollment(section)
    session.add(section)
    session.flush()

def add_student(session: Session):
    """
    Prompt the user for the information for a new student and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_email: bool = False
    last_name: str = ''
    first_name: str = ''
    email: str = ''
    while not unique_email or not unique_name:
        last_name = input("Student last name--> ")
        first_name = input("Student first name-->")
        email = input("Student e-mail address--> ")
        name_count: int = session.query(Student).filter(Student.lastName == last_name,
                                                        Student.firstName == first_name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a student by that name.  Try again.")
        if unique_name:
            email_count = session.query(Student).filter(Student.email == email).count()
            unique_email = email_count == 0
            if not unique_email:
                print("We already have a student with that email address.  Try again.")
    new_student = Student(last_name, first_name, email)
    session.add(new_student)


def add_student_section(session: Session):
    """Enroll a student in a section
    AKA adds a student to the section list of enrolled students
    """
    section: Section = select_section(session)
    student: Student = select_student(session)

    student_section_count: int = session.query(Enrollment).filter(
        # Cant be enrolled in same section twice
        Enrollment.studentID == student.studentID,
        Enrollment.sectionYear== section.sectionYear,
        Enrollment.semester == section.semester,
        Enrollment.courseNumber == section.courseNumber,
        Enrollment.departmentAbbreviation==section.departmentAbbreviation
    ).count()

    unique_student_section: bool = student_section_count == 0
    while not unique_student_section:
        print("That student is already enrolled in that section. Try again.")
        student = select_student(session)
        section = select_section(session)
    # Maps enrollment instance to section
    section.add_enrollment(student)
    # Add enrollment instance to the session
    session.add(section)
    session.flush()


def add_student_major(sess: Session):
    student: Student = select_student(sess)
    major: Major = select_major(sess)
    student_major_count: int = sess.query(StudentMajor).filter(StudentMajor.studentId == student.studentID,
                                                               StudentMajor.majorName == major.name).count()
    unique_student_major: bool = student_major_count == 0
    while not unique_student_major:
        print("That student already has that major.  Try again.")
        student = select_student(sess)
        major = select_major(sess)
    student.add_major(major)
    """The student object instance is mapped to a specific row in the Student table.  But adding
    the new major to its list of majors does not add the new StudentMajor instance to this session.
    That StudentMajor instance was created and added to the Student's majors list inside of the
    add_major method, but we don't have easy access to it from here.  And I don't want to have to 
    pass sess to the add_major method.  So instead, I add the student to the session.  You would
    think that would cause an insert, but SQLAlchemy is smart enough to know that this student 
    has already been inserted, so the add method takes this to be an update instead, and adds
    the new instance of StudentMajor to the session.  THEN, when we flush the session, that 
    transient instance of StudentMajor gets inserted into the database, and is ready to be 
    committed later (which happens automatically when we exit the application)."""
    sess.add(student)                           # add the StudentMajor to the session
    sess.flush()


def add_major(session: Session):
    """
    Prompt the user for the information for a new major and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this major?")
    department: Department = select_department(session)
    unique_name: bool = False
    name: str = ''
    while not unique_name:
        name = input("Major name--> ")
        name_count: int = session.query(Major).filter(Major.departmentAbbreviation == department.abbreviation,
                                                      ).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a major by that name in that department.  Try again.")
    description: str = input('Please give this major a description -->')
    major: Major = Major(department, name, description)
    session.add(major)


def add_major_student(sess: Session):
    major: Major = select_major(sess)
    student: Student = select_student(sess)
    student_major_count: int = sess.query(StudentMajor).filter(StudentMajor.studentId == student.studentID,
                                                               StudentMajor.majorName == major.name).count()
    unique_student_major: bool = student_major_count == 0
    while not unique_student_major:
        print("That major already has that student.  Try again.")
        major = select_major(sess)
        student = select_student(sess)
    major.add_student(student)
    """The major object instance is mapped to a specific row in the Major table.  But adding
    the new student to its list of students does not add the new StudentMajor instance to this session.
    That StudentMajor instance was created and added to the Major's students list inside of the
    add_student method, but we don't have easy access to it from here.  And I don't want to have to 
    pass sess to the add_student method.  So instead, I add the major to the session.  You would
    think that would cause an insert, but SQLAlchemy is smart enough to know that this major 
    has already been inserted, so the add method takes this to be an update instead, and adds
    the new instance of StudentMajor to the session.  THEN, when we flush the session, that 
    transient instance of StudentMajor gets inserted into the database, and is ready to be 
    committed later (which happens automatically when we exit the application)."""
    sess.add(major)                           # add the StudentMajor to the session
    sess.flush()


