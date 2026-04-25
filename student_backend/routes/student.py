from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
from typing import List

router = APIRouter(prefix="/students", tags=["Students"])


# ✅ CREATE STUDENT
@router.post(
    "/", 
    response_model=schemas.StudentResponse,   # ✅ FIXED
    status_code=status.HTTP_201_CREATED
)
def create(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)


# ✅ GET ALL STUDENTS
@router.get(
    "/", 
    response_model=List[schemas.StudentResponse]   # ✅ FIXED
)
def get_all(db: Session = Depends(get_db)):
    return crud.get_students(db)


# ✅ GET STUDENT BY ID
@router.get(
    "/{student_id}", 
    response_model=schemas.StudentResponse   # ✅ FIXED
)
def get_one(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student_by_id(db, student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


# ✅ FULL UPDATE (PUT)
@router.put(
    "/{student_id}", 
    response_model=schemas.StudentResponse
)
def update(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    updated = crud.update_student(db, student_id, student)

    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")

    return updated


# ✅ PARTIAL UPDATE (PATCH)
@router.patch(
    "/{student_id}", 
    response_model=schemas.StudentResponse
)
def partial_update(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    updated = crud.update_student(db, student_id, student)

    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")

    return updated


# ✅ DELETE STUDENT
@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)  # ✅ improved
def delete(student_id: int, db: Session = Depends(get_db)):
    student = crud.delete_student(db, student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return