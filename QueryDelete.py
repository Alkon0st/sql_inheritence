from Section import Section
from Department import Department
from Course import Course
from Student import Student
from Major import Major
from Enrollment import Enrollment
from QuerySelect import select_course, select_department, select_major, select_section, select_student
from db_connection import Session


def delete_section(sess: Session):
    """
    Delete a section if no students are enrolled
    """
    print("Deleting a section")
    # Select the section to delete
    section = select_section(sess)  # Assuming you have a function to select a section
    
    # Query enrollments associated with the section
    n_enrollments = sess.query(Enrollment).filter(Enrollment.section == section).count()
    
    if n_enrollments > 0:
        print(f"Sorry, there are {n_enrollments} students enrolled in that section. Delete the enrollments first.")
    else:
        sess.delete(section)
        print("Section deleted successfully from session")

def delete_student(sess: Session):
    """
    Delete a student if not enrolled in any sections.
    """
    print("Deleting a student")
    # Select the student to delete
    student: Student = select_student(sess)  # Assuming you have a function to select a student
    
    # Query enrollments associated with the student
    n_enrollments = sess.query(Enrollment).filter(Enrollment.studentId == student.studentID).count()

    if n_enrollments > 0:
        print(f"Sorry, the student is enrolled in {n_enrollments} section(s). Please remove enrollments first.")
    else:
        sess.delete(student)
        print("Student deleted successfully.")



def delete_department(session: Session):
    """
    Prompt the user for a department by the abbreviation and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a department")
    department: Department = select_department(session)
    n_courses = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation).count()
    if n_courses > 0:
        print(f"Sorry, there are {n_courses} courses in that department.  Delete them first, "
              "then come back here to delete the department.")
    else:
        session.delete(department)


def delete_course(session: Session):
    """
    Prompt the user to select a course by department abbreviation and course number, then delete it.
    :param session: The connection to the database.
    :return: None
    """
    print("Deleting a course")
    course: Course = select_course(session)
    n_sections = session.query(Section).filter(Section.courseNumber == course.courseNumber).count()
    if n_sections>0:
        print(f"Sorry, there are {n_sections} sections in that course. Delete them first, "
              "then come back here to delete the course")
    else:
        session.delete(course)



def delete_student_section(sess: Session):
    """Remove section from a student that its enrolled in"""
    print("Prompting you for the student who is unenrolling from section")
    student: Student = select_student(sess)
    section: Section = select_section(sess)
    student.remove_enrollment(section)


def delete_section_student(sess: Session):
    """Drop/remove a student from a section its enrolled in"""
    print("Prompting you for section that is dropping the enrolled student")
    section: Section = select_section(sess)
    student: Student = select_student(sess)
    section.remove_enrollment(student)


def delete_major_student(sess: Session):
    """Remove a student from a particular major.
    :param sess:    The current database session.
    :return:        None
    """
    print("Prompting you for the major and the student who no longer has that major.")
    major: Major = select_major(sess)
    student: Student = select_student(sess)
    major.remove_student(student)


def delete_student_major(sess: Session):
    """Undeclare a student from a particular major.
    :param sess:    The current database session.
    :return:        None
    """
    print("Prompting you for the student and the major that they no longer have.")
    student: Student = select_student(sess)
    major: Major = select_major(sess)
    student.remove_major(major)






