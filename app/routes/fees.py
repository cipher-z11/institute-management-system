# updated: 2026-05-14
# fix: code cleanup and remove unused imports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.database import get_db
from app.models.models import Fee, FeeStatusEnum
from app.schemas.schemas import FeeCreate, FeeUpdate, FeeResponse

router = APIRouter()


def compute_status(amount_due: float, amount_paid: float) -> FeeStatusEnum:
    if amount_paid <= 0:
        return FeeStatusEnum.pending
    elif amount_paid >= amount_due:
        return FeeStatusEnum.paid
    return FeeStatusEnum.partial


@router.post("/", response_model=FeeResponse, status_code=status.HTTP_201_CREATED)
def create_fee(fee: FeeCreate, db: Session = Depends(get_db)):
    db_fee = Fee(
        **fee.model_dump(),
        status=compute_status(fee.amount_due, fee.amount_paid or 0.0)
    )
    db.add(db_fee)
    db.commit()
    db.refresh(db_fee)
    return db_fee


@router.get("/student/{student_id}", response_model=List[FeeResponse])
def get_fees_by_student(student_id: int, db: Session = Depends(get_db)):
    return db.query(Fee).filter(Fee.student_id == student_id).all()


@router.put("/{fee_id}/pay", response_model=FeeResponse)
def pay_fee(fee_id: int, update: FeeUpdate, db: Session = Depends(get_db)):
    fee = db.query(Fee).filter(Fee.id == fee_id).first()
    if not fee:
        raise HTTPException(status_code=404, detail="Fee record not found")
    fee.amount_paid = update.amount_paid
    fee.paid_date = update.paid_date or date.today()
    fee.status = compute_status(fee.amount_due, fee.amount_paid)
    db.commit()
    db.refresh(fee)
    return fee


@router.get("/pending", response_model=List[FeeResponse])
def get_pending_fees(db: Session = Depends(get_db)):
    return db.query(Fee).filter(Fee.status != FeeStatusEnum.paid).all()
