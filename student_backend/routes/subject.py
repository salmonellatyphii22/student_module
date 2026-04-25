from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter(prefix="/subjects", tags=["Subjects"])


# ✅ CREATE SUBJECT
@router.post("/", response_model=schemas.SubjectResponse, status_code=status.HTTP_201_CREATED)
def create(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    return crud.create_subject(db, subject)


# ✅ GET ALL SUBJECTS
@router.get("/", response_model=List[schemas.SubjectResponse])
def get_all(db: Session = Depends(get_db)):
    return crud.get_subjects(db)


# ✅ GET SUBJECT BY ID
@router.get("/{subject_id}", response_model=schemas.SubjectResponse)
def get_one(subject_id: int, db: Session = Depends(get_db)):
    subject = crud.get_subject_by_id(db, subject_id)

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    return subject


# ✅ UPDATE SUBJECT (PUT)
@router.put("/{subject_id}", response_model=schemas.SubjectResponse)
def update(subject_id: int, subject: schemas.SubjectUpdate, db: Session = Depends(get_db)):
    updated = crud.update_subject(db, subject_id, subject)

    if not updated:
        raise HTTPException(status_code=404, detail="Subject not found")

    return updated


# ✅ PARTIAL UPDATE (PATCH)
@router.patch("/{subject_id}", response_model=schemas.SubjectResponse)
def partial_update(subject_id: int, subject: schemas.SubjectUpdate, db: Session = Depends(get_db)):
    updated = crud.update_subject(db, subject_id, subject)

    if not updated:
        raise HTTPException(status_code=404, detail="Subject not found")

    return updated


# ✅ DELETE SUBJECT
@router.delete("/{subject_id}")
def delete(subject_id: int, db: Session = Depends(get_db)):
    subject = crud.delete_subject(db, subject_id)

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    return {"message": "Subject deleted successfully"}