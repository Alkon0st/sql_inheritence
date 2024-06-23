from orm_base import Base
from db_connection import engine
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint, CheckConstraint
from sqlalchemy import String, Integer, Time
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import Table
from constants import START_OVER, REUSE_NO_INTROSPECTION, INTROSPECT_TABLES
from datetime import datetime
from Course import Course
from Enrollment import Enrollment

class Section(Base):
    """
    Section - when, where, and whom is teaching a course at a department. 
    Associated many to one with course, and many to many
    with student via enrollment lookup table
    """
    __tablename__ = "sections" # The physical name of this table
    # PRIMARY KEYS
    departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', primary_key=True)
    courseNumber: Mapped[int] = mapped_column('course_number', primary_key=True)
    sectionNumber: Mapped[int] = mapped_column('section_number', Integer, nullable=False, primary_key=True)
    semester: Mapped[str] = mapped_column('semester', String(10), nullable=False, primary_key=True)
    sectionYear: Mapped[int] = mapped_column('section_year', Integer, nullable=False, primary_key=True)
    # Rest of columns (Non primary)
    building: Mapped[str] = mapped_column('building', String(6), nullable=False)
    room: Mapped[int] = mapped_column('room', Integer, nullable=False)
    schedule: Mapped[str] = mapped_column('schedule', String(6)) 
    startTime: Mapped[Time] = mapped_column('start_time', Time) # How the hell does this work for input??
    instructor: Mapped[str] = mapped_column('instructor', String(80), nullable=False)
    # Relationships
    course: Mapped["Course"] = relationship(
        # 1 course -> * sections bidirectional
        back_populates="sections"
    )
    students: Mapped[List["Enrollment"]]= relationship(    
        # Many to many with sections throuigh Enrollments
        "Enrollment", back_populates = "section", cascade="all, save-update, delete-orphan"
    )
    __table_args__ = (
        # Candidate key 1: room cannot be occupied by more than one section at the same time, 
        # Candidate key 2: instructor can't teach two sections at the same time
        UniqueConstraint("section_year", "semester", "schedule", "start_time", "building", "room", name="section_uk_01"),
        UniqueConstraint("section_year", "semester", "schedule", "start_time", "instructor", name="section_uk_02"), 
        # Ensure valid input
        CheckConstraint(semester.in_(["Fall", "Spring", "Winter", "Summer I", "Summer II"])),
        CheckConstraint(schedule.in_(["MW", "TuTh", "MWF", "F", "S"])),
        CheckConstraint(building.in_(["VEC", "ECS", "EN2", "EN3", "EN4", "ET", "SSPA"])),
        # Course (Parent) contains two primary keys. Referencing mapped_column and not attribute here
        ForeignKeyConstraint(
            # Migrating FKs from course, also PKs to identify section
            [departmentAbbreviation, courseNumber], 
            [Course.departmentAbbreviation, Course.courseNumber]
        )
    )
    
    
    def __init__(self, course: Course, sectionNumber: int, semester: str, sectionYear: int,  
                     building: str, room: int, schedule: str, startTime: Time, instructor: str):
        self.set_course(course)
        self.sectionNumber = sectionNumber
        self.semester = semester
        self.sectionYear = sectionYear
        self.building = building
        self.room = room
        self.schedule = schedule
        self.startTime = startTime
        self.instructor = instructor


    def set_course(self, course: Course):
        """
        This basically ensures we have a course regardless of constraints
        of said course, otherwise it complains about creating a section object
        course is made which it depends on. SQL alchemy takes care of this
        """
        self.course = course
        self.departmentAbbreviation = course.departmentAbbreviation
        self.courseNumber = course.courseNumber

    
    def add_enrollment(self, student):
        """    
        Adds enrollment of student to the list of students enrolled in the section
        Note: not creating a student but rather keeping track of its instance
        association 
        
        """
        # Make sure that this section does not already have this Student.
        for next_student in self.students:
            if next_student.student == student:
                return              # This student is already in this section
        # create the necessary Association Class instance that connects This section to
        # the supplied student.
        student_enrollment = Enrollment(student, self, datetime.now())
        student.section.append(student_enrollment)        # Add this new junction entry to the Student
        self.students.append(student_enrollment)         # Add this new junction entry to this Section

    
    def remove_enrollment(self, student):
        """
        Removes a student from the enrolled students in the section
        Assuming you found the student in the section 
        """
        for next_student in self.students:
            if next_student.student == student:
                # Remove this student from the section's list of students
                self.students.remove(next_student)
                return

        
    def __str__(self):
        return f"{self.semester}, {self.sectionYear}, Section: {self.sectionNumber}, \nRoom: {self.building} {self.room} \nSchedule: {self.schedule} {self.startTime} Instructor: {self.instructor}"
    


    

