from Department import Department
from Course import Course
from Section import Section 
from Student import Student
from Major import Major
from StudentMajor import StudentMajor
from Enrollment import Enrollment
from QuerySelect import select_department, select_section, select_student, select_major
from db_connection import Session

def list_enrollments():
    enrollments = get_all_enrollments()  # Assuming a function that fetches all enrollments
    for enrollment in enrollments:
        if enrollment.grade_type == 'PassFail':
            print(enrollment)
        elif enrollment.grade_type == 'LetterGrade':
            print(enrollment)
            
            
def list_department(session: Session):
    """
    List all departments, sorted by the abbreviation.
    :param session:     The connection to the database.
    :return:            None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    departments: [Department] = list(session.query(Department).order_by(Department.abbreviation))
    for department in departments:
        print(department)


def list_department_courses(sess: Session):
    """
    List all courses department offers
    """
    department = select_department(sess)
    dept_courses: [Course] = department.get_courses()
    print("Course for department: " + str(department))
    for dept_course in dept_courses:
        print(dept_course)


def list_course(sess: Session):
    """
    List all courses currently in the database.
    :param sess:    The connection to the database.
    :return:        None
    """
    courses: [Course] = list(sess.query(Course).order_by(Course.courseNumber))
    for course in courses:
        print(course)


def list_section(session: Session):
    """
    List all sections currently in database
    """
    sections: [Section] = list(session.query(Section).order_by(Section.sectionNumber))
    for section in sections:
        print(section)


def list_section_student(sess: Session):
    """
    List all students enrolled in a given section.
    :param sess: SQLAlchemy session object.
    :param section: The section object for which students need to be listed.
    :return: None
    """
    section = select_section(sess)
    # Query all students enrolled in the given section
    students = sess.query(Student).join(
        Enrollment, Enrollment.studentId == Student.studentID).filter(
        Enrollment.section == section).all()

    # Print out the details of each student
    for student in students:
        print(f"Student name: {student.lastName}, {student.firstName}")


def list_student(sess: Session):
    """
    List all Students currently in the database.
    :param sess:    The current connection to the database.
    :return:
    """
    students: [Student] = list(sess.query(Student).order_by(Student.lastName, Student.firstName))
    for student in students:
        print(student)


def list_student_section(sess: Session):
    """
    Prompt the user for the student, then list the sections 
    that the student is enrolled in.
    departmentAbbreviation, courseNumber, sectionYear, semester, studentId

    filter list by student
    """
    student: Student = select_student(sess)
    # Join Enrollment to Student, then to section
    recs = sess.query(Student).join(
        Enrollment, Student.studentID == Enrollment.studentId).join(
        Section, Enrollment.section).filter(
                Student.studentID == student.studentID).add_columns(
                    Section.departmentAbbreviation, Section.sectionNumber, 
                    Section.sectionYear, Section.semester, Section.courseNumber).all()
    for sec in recs:
        print(f"{sec.departmentAbbreviation} {sec.courseNumber} {sec.semester} {sec.sectionYear}  Section: {sec.sectionNumber}")



def list_student_major(sess: Session):
    """Prompt the user for the student, and then list the majors that the student has declared.
    :param sess:    The connection to the database
    :return:        None
    """
    student: Student = select_student(sess)
    recs = sess.query(Student).join(StudentMajor, Student.studentID == StudentMajor.studentId).join(
        Major, StudentMajor.majorName == Major.name).filter(
        Student.studentID == student.studentID).add_columns(
        Student.lastName, Student.firstName, Major.description, Major.name).all()
    for stu in recs:
        print(f"Student name: {stu.lastName}, {stu.firstName}, Major: {stu.name}, Description: {stu.description}")



def list_major(sess: Session):
    """
    List all majors in the database.
    :param sess:    The current connection to the database.
    :return:
    """
    majors: [Major] = list(sess.query(Major).order_by(Major.departmentAbbreviation))
    for major in majors:
        print(major)


def list_major_student(sess: Session):
    """Prompt the user for the major, then list the students who have that major declared.
    :param sess:    The connection to the database.
    :return:        None
    """
    major: Major = select_major(sess)
    recs = sess.query(Major).join(StudentMajor, StudentMajor.majorName == Major.name).join(
        Student, StudentMajor.studentId == Student.studentID).filter(
        Major.name == major.name).add_columns(
        Student.lastName, Student.firstName, Major.description, Major.name).all()
    for stu in recs:
        print(f"Student name: {stu.lastName}, {stu.firstName}, Major: {stu.name}, Description: {stu.description}")
