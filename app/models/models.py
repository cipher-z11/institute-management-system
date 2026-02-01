from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(15))
    gender = Column(SAEnum(GenderEnum))
    date_of_birth = Column(Date)
    address = Column(String(300))
    enrollment_number = Column(String(50), unique=True, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"))

    course = relationship("Course", back_populates="students")
    fees = relationship("Fee", back_populates="student")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    duration_years = Column(Integer)
    total_seats = Column(Integer)
    department = Column(String(100))
    faculty_id = Column(Integer, ForeignKey("faculty.id"), nullable=True)

    students = relationship("Student", back_populates="course")
    faculty = relationship("Faculty", back_populates="courses")


class Faculty(Base):
    __tablename__ = "faculty"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(15))
    department = Column(String(100))
    designation = Column(String(100))
    qualification = Column(String(150))
    experience_years = Column(Integer, default=0)

    courses = relationship("Course", back_populates="faculty")


class FeeStatusEnum(str, enum.Enum):
    paid = "paid"
    pending = "pending"
    partial = "partial"


class Fee(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    semester = Column(Integer)
    amount_due = Column(Float, nullable=False)
    amount_paid = Column(Float, default=0.0)
    status = Column(SAEnum(FeeStatusEnum), default=FeeStatusEnum.pending)
    due_date = Column(Date)
    paid_date = Column(Date, nullable=True)

    student = relationship("Student", back_populates="fees")
