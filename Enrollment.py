from sqlalchemy import ForeignKey, Date, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from orm_base import Base
from datetime import datetime


class Enrollment(Base):
    """
    The association class between Student and Section
    """
    __tablename__ = "enrollments"
    # Relationships - child to section and student
    section: Mapped["Section"] = relationship("Section", back_populates="students")  
    student: Mapped["Student"] = relationship("Student", back_populates="sections") 
    """Without a surrogate, I used all FKs and set them as a composite PK so that 
    you can do the relationship between student and section.
    """
    # Migrating FK from student, only one
    studentId: Mapped[int] = mapped_column('student_id', ForeignKey("students.student_id"), primary_key=True)
    # Migrating FKs from Section
    departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation',primary_key=True)
    courseNumber: Mapped[int] = mapped_column('course_number', primary_key=True)
    sectionNumber: Mapped[int] = mapped_column('section_number', primary_key=True)
    semester: Mapped[str] = mapped_column('semester', primary_key=True)
    sectionYear: Mapped[int] = mapped_column('section_year', primary_key=True)
    
    enrollmentDate: Mapped[Date] = mapped_column('declaration_date', Date, nullable=False)

    type: Mapped[str] = mapped_column("type", String(50), nullable=False)
    __table_args__ = (
        # Unique constraint to ensure a student cannot enroll in the same course more than once per semester
        UniqueConstraint(
            'department_abbreviation', 'course_number', 'section_year', 'semester', 'student_id',
            name='enrollment_uk_01'
        ),
        # 5 Migrating FKs from Section(Parent)
        ForeignKeyConstraint(
            ['department_abbreviation', 'course_number', 'section_number', 'semester', 'section_year'],
            ['sections.department_abbreviation', 'sections.course_number', 'sections.section_number', 'sections.semester', 'sections.section_year'],
            name = "enrollments_sections_fk_01"
        ),
    )
    # Polymorphism stuff
    __mapper_args__ = {
         "polymorphic_identity": "enrollment", "polymorphic_on": "type"
     }

    def __init__(self, student, section, enrollment_date: datetime):
        # init student values
        self.student = student
        self.studentId = student.studentID
        # init section values
        self.section = section
        self.departmentAbbreviation = section.departmentAbbreviation
        self.courseNumber = section.courseNumber
        self.sectionNumber = section.sectionNumber
        self.semester = section.semester
        self.sectionYear = section.sectionYear
        self.enrollmentDate = enrollment_date


    def __str__(self):
        return f"Enrollment- section: {self.student} section: {self.section}"
