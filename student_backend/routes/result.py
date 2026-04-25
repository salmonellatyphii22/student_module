from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud

router = APIRouter()

@router.get("/{student_id}")
def result(student_id: int, db: Session = Depends(get_db)):
    return crud.get_student_result(db, student_id)