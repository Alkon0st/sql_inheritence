from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped


class LetterGrade(Enrollment):
    __tablename__ = "letter_grade"
    letterGradeId: Mapped[int] = mapped_column(
        "letter_grade_id", ForeignKey("enrollments.enrollment_id", ondelete="CASCADE"), primary_key=True
    )
    minSatisfactory: Mapped[str] = mapped_column("min_satisfactory", String(1))
    grade: Mapped[str] = mapped_column("grade", String(1))
    __mapper_args__ = {"polymorphic_identity": "letter_grade"}

    def __init__(self, section, student, min_satisfactory: str, grade: str):
        super().__init__(section, student)
        self.minSatisfactory = min_satisfactory.upper()  # Make sure the minSatisfactory grade is in uppercase
        self.grade = grade.upper()  # Make sure the grade is in uppercase

        if self.minSatisfactory not in {"A", "B", "C", "D", "F"}:
            raise ValueError(f"minSatisfactory must be one of: A, B, C, D, F, but was {self.minSatisfactory}")

        if self.grade not in {"A", "B", "C", "D", "F"}:
            raise ValueError(f"grade must be one of: A, B, C, D, F, but was {self.grade}")

    def __str__(self):
        return f"LetterGrade Enrollment: {super().__str__()}"

