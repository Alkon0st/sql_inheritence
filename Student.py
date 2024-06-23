

from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List                 # Use this for the list of Majors that this student has
from StudentMajor import StudentMajor
from Enrollment import Enrollment
from datetime import datetime


class Student(Base):
    """An individual who may or may not be enrolled at the university, who
    enrolls in courses toward some educational objective. That objective
    could be a formal degree program, or it could be a specialized certificate."""
    __tablename__ = "students"
    # Let SQLAlchemy handle the generation of student_id values for us.
    studentID: Mapped[int] = mapped_column('student_id', Integer, Identity(start=1, cycle=True), primary_key=True)
    lastName: Mapped[str] = mapped_column('last_name', String(50), nullable=False, primary_key=False)
    firstName: Mapped[str] = mapped_column('first_name', String(50), nullable=False, primary_key=False)
    email: Mapped[str] = mapped_column('email', String(255), nullable=False)
    # Relationships
    majors: Mapped[List["StudentMajor"]] = relationship(
        "StudentMajor", back_populates="student", cascade="all, save-update, delete-orphan"
    )
    sections: Mapped[List["Enrollment"]] = relationship(
        "Enrollment", back_populates="student", cascade="all, save-update, delete-orphan"
    )
    #Constraints
    __table_args__ = (
        UniqueConstraint("first_name", "last_name", name="students_uk_01"),
        UniqueConstraint("email", name="students_uk_02")
    )


    def __init__(self, lastName: str, firstName: str, email: str):
        self.lastName = lastName
        self.firstName = firstName
        self.email = email


    # add/remove sections in student list
    def add_enrollment(self, section):
        """Add a section instance to a list of sections the student 
        is enrolled in currently.
        """
        for next_section in self.sections:
            if next_section.section == section:
                return  # Student already enrolled in section
        student_enrollment = Enrollment(self, section, datetime.now())
        section.students.append(student_enrollment)
        self.sections.append(student_enrollment)

    
    def remove_enrollment(self, section):
        """Remove a section instance from the list of sections 
        the student is enrolled in.
        """
        for next_section in self.sections:
            if next_section.section == section:
                self.sections.remove(next_section)
                return


    def add_major(self, major):
        """Add a new major to the student.  We are not actually adding a major directly
        to the student.  Rather, we are adding an instance of StudentMajor to the student.
        :param  major:  The Major that this student has declared.
        :return:        None
        """
        # Make sure that this student does not already have this major.
        for next_major in self.majors:
            if next_major.major == major:
                return                  # This student already has this major
        # Create the new instance of StudentMajor to connect this Student to the supplied Major.
        student_major = StudentMajor(self, major, datetime.now())
        major.students.append(student_major)                # Add this Student to the supplied Major.
        self.majors.append(student_major)                   # Add the supplied Major to this student.


    def remove_major(self, major):
        """
        Remove a major from the list of majors that a student presently has declared.
        Essentially, we are UNdeclaring the major.  A bit contrived, but this is for
        demonstration purposes.
        :param major:
        :return:
        """
        for next_major in self.majors:
            # This item in the list is the major we are looking for for this student.
            if next_major.major == major:
                self.majors.remove(next_major)
                return


    def __str__(self):
        return f"Student ID: {self.studentID} name: {self.lastName}, {self.firstName} e-mail: {self.email}"