from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
from typing import List
from dependencies import require_faculty, allow_view

router = APIRouter(prefix="/faculty", tags=["Faculty"])


# ✅ CREATE → ONLY FACULTY/ADMIN
@router.post(
    "/", 
    response_model=schemas.FacultyResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_faculty)]
)
def create(faculty: schemas.FacultyCreate, db: Session = Depends(get_db)):
    return crud.create_faculty(db, faculty)


# ✅ VIEW ALL → STUDENT + FACULTY
@router.get(
    "/", 
    response_model=List[schemas.FacultyResponse],
    dependencies=[Depends(allow_view)]
)
def get_all(db: Session = Depends(get_db)):
    return crud.get_faculties(db)


# ✅ VIEW ONE → STUDENT + FACULTY
@router.get(
    "/{Faculty_ID}", 
    response_model=schemas.FacultyResponse,
    dependencies=[Depends(allow_view)]
)
def get_one(Faculty_ID: int, db: Session = Depends(get_db)):
    faculty = crud.get_faculty_by_id(db, Faculty_ID)

    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    return faculty


# ❌ UPDATE → ONLY FACULTY
@router.put(
    "/{Faculty_ID}", 
    response_model=schemas.FacultyResponse,
    dependencies=[Depends(require_faculty)]
)
def update(Faculty_ID: int, faculty: schemas.FacultyUpdate, db: Session = Depends(get_db)):
    updated = crud.update_faculty(db, Faculty_ID, faculty)

    if not updated:
        raise HTTPException(status_code=404, detail="Faculty not found")

    return updated


# ❌ PARTIAL UPDATE → ONLY FACULTY
@router.patch(
    "/{Faculty_ID}", 
    response_model=schemas.FacultyResponse,
    dependencies=[Depends(require_faculty)]
)
def partial_update(Faculty_ID: int, faculty: schemas.FacultyUpdate, db: Session = Depends(get_db)):
    updated = crud.update_faculty(db, Faculty_ID, faculty)

    if not updated:
        raise HTTPException(status_code=404, detail="Faculty not found")

    return updated


# ❌ DELETE → ONLY FACULTY
@router.delete(
    "/{Faculty_ID}", 
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_faculty)]
)
def delete(Faculty_ID: int, db: Session = Depends(get_db)):
    faculty = crud.delete_faculty(db, Faculty_ID)

    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    return