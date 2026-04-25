from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db

router = APIRouter()

@router.post("/")
def enroll(data: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    return crud.enroll_student(db, data)