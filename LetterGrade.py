from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from Enrollment import Enrollment

class LetterGrade(Enrollment):
    __tablename__ = 'letter_grade'
    id = mapped_column(Integer, ForeignKey('enrollments.id', ondelete='CASCADE'), primary_key=True)
    min_satisfactory = mapped_column(String, nullable=False)

    __table_args__ = (
        CheckConstraint(min_satisfactory.in_({'A', 'B', 'C', 'D', 'F'}), name='check_min_satisfactory'),
    )

    __mapper_args__ = {
        'polymorphic_identity': 'letter_grade',
    }

    def __init__(self, student, section, enrollment_date: datetime, min_satisfactory: str):
        super().__init__(student, section, enrollment_date)
        if min_satisfactory not in {'A', 'B', 'C', 'D', 'F'}:
            raise ValueError("Invalid min_satisfactory value")
        self.min_satisfactory = min_satisfactory