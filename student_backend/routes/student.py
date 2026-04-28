from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
from typing import List
from dependencies import require_faculty, allow_view

router = APIRouter(prefix="/students", tags=["Students"])


# ❌ CREATE → ONLY FACULTY
@router.post(
    "/", 
    response_model=schemas.StudentResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_faculty)]
)
def create(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)


# ✅ VIEW ALL → STUDENT + FACULTY + ADMIN
@router.get(
    "/", 
    response_model=List[schemas.StudentResponse],
    dependencies=[Depends(allow_view)]   # ✅ FIXED
)
def get_all(db: Session = Depends(get_db)):
    return crud.get_students(db)


# ✅ VIEW BY ID → ALL LOGGED USERS
@router.get(
    "/{student_id}", 
    response_model=schemas.StudentResponse,
    dependencies=[Depends(allow_view)]   # ✅ FIXED
)
def get_one(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student_by_id(db, student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


# ❌ UPDATE → ONLY FACULTY
@router.put(
    "/{student_id}", 
    response_model=schemas.StudentResponse,
    dependencies=[Depends(require_faculty)]
)
def update(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    updated = crud.update_student(db, student_id, student)

    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")

    return updated


# ❌ PARTIAL UPDATE → ONLY FACULTY
@router.patch(
    "/{student_id}", 
    response_model=schemas.StudentResponse,
    dependencies=[Depends(require_faculty)]
)
def partial_update(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    updated = crud.update_student(db, student_id, student)

    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")

    return updated


# ❌ DELETE → ONLY FACULTY
@router.delete(
    "/{student_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_faculty)]
)
def delete(student_id: int, db: Session = Depends(get_db)):
    student = crud.delete_student(db, student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return