# fix: implement Fee management with status tracking
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from app.models.models import GenderEnum, FeeStatusEnum


# ── Student Schemas ──────────────────────────────────────────────────────────
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    gender: Optional[GenderEnum] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    enrollment_number: str
    course_id: Optional[int] = None


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    course_id: Optional[int] = None


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    enrollment_number: str
    course_id: Optional[int] = None

    class Config:
        from_attributes = True


# ── Course Schemas ───────────────────────────────────────────────────────────
class CourseCreate(BaseModel):
    name: str
    code: str
    duration_years: Optional[int] = None
    total_seats: Optional[int] = None
    department: Optional[str] = None
    faculty_id: Optional[int] = None


class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    department: Optional[str] = None

    class Config:
        from_attributes = True


# ── Faculty Schemas ──────────────────────────────────────────────────────────
class FacultyCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    qualification: Optional[str] = None
    experience_years: Optional[int] = 0


class FacultyResponse(BaseModel):
    id: int
    name: str
    email: str
    department: Optional[str] = None
    designation: Optional[str] = None

    class Config:
        from_attributes = True


# ── Fee Schemas ──────────────────────────────────────────────────────────────
class FeeCreate(BaseModel):
    student_id: int
    semester: int
    amount_due: float
    amount_paid: Optional[float] = 0.0
    due_date: Optional[date] = None


class FeeUpdate(BaseModel):
    amount_paid: float
    paid_date: Optional[date] = None


class FeeResponse(BaseModel):
    id: int
    student_id: int
    semester: int
    amount_due: float
    amount_paid: float
    status: FeeStatusEnum

    class Config:
        from_attributes = True


# ── RAG Schemas ──────────────────────────────────────────────────────────────
class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[str] = []
