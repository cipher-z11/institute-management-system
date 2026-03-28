from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Faculty
from app.schemas.schemas import FacultyCreate, FacultyResponse

router = APIRouter()


@router.post("/", response_model=FacultyResponse, status_code=status.HTTP_201_CREATED)
def create_faculty(faculty: FacultyCreate, db: Session = Depends(get_db)):
    existing = db.query(Faculty).filter(Faculty.email == faculty.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Faculty with this email already exists.")
    db_faculty = Faculty(**faculty.model_dump())
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty


@router.get("/", response_model=List[FacultyResponse])
def get_all_faculty(db: Session = Depends(get_db)):
    return db.query(Faculty).all()


@router.get("/{faculty_id}", response_model=FacultyResponse)
def get_faculty(faculty_id: int, db: Session = Depends(get_db)):
    f = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return f


@router.delete("/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faculty(faculty_id: int, db: Session = Depends(get_db)):
    f = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Faculty not found")
    db.delete(f)
    db.commit()

# Write README and API documentation
