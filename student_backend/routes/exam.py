from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
from typing import List
from dependencies import require_faculty, allow_view

router = APIRouter(prefix="/exams", tags=["Exams"])


# ✅ CREATE EXAM → ONLY FACULTY
@router.post(
    "/", 
    response_model=schemas.ExamResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_faculty)]
)
def create(exam: schemas.ExamCreate, db: Session = Depends(get_db)):
    return crud.create_exam(db, exam)


# ✅ GET ALL EXAMS → STUDENT + FACULTY
@router.get(
    "/", 
    response_model=List[schemas.ExamResponse],
    dependencies=[Depends(allow_view)]
)
def get_all(db: Session = Depends(get_db)):
    return crud.get_exams(db)


# ✅ GET EXAM BY ID
@router.get(
    "/{exam_id}", 
    response_model=schemas.ExamResponse,
    dependencies=[Depends(allow_view)]
)
def get_one(exam_id: int, db: Session = Depends(get_db)):
    exam = crud.get_exam_by_id(db, exam_id)

    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    return exam


# ❌ UPDATE EXAM → ONLY FACULTY
@router.put(
    "/{exam_id}", 
    response_model=schemas.ExamResponse,
    dependencies=[Depends(require_faculty)]
)
def update(exam_id: int, exam: schemas.ExamUpdate, db: Session = Depends(get_db)):
    updated = crud.update_exam(db, exam_id, exam)

    if not updated:
        raise HTTPException(status_code=404, detail="Exam not found")

    return updated


# ❌ PARTIAL UPDATE
@router.patch(
    "/{exam_id}", 
    response_model=schemas.ExamResponse,
    dependencies=[Depends(require_faculty)]
)
def partial_update(exam_id: int, exam: schemas.ExamUpdate, db: Session = Depends(get_db)):
    updated = crud.update_exam(db, exam_id, exam)

    if not updated:
        raise HTTPException(status_code=404, detail="Exam not found")

    return updated


# ❌ DELETE EXAM → ONLY FACULTY
@router.delete(
    "/{exam_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_faculty)]
)
def delete(exam_id: int, db: Session = Depends(get_db)):
    exam = crud.delete_exam(db, exam_id)

    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    return