from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
from typing import List
from dependencies import require_faculty, allow_view

router = APIRouter(prefix="/courses", tags=["Courses"])


# ❌ CREATE → ONLY FACULTY
@router.post(
    "/", 
    response_model=schemas.CourseResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_faculty)]
)
def create(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, course)


# ✅ VIEW ALL → STUDENT + FACULTY
@router.get(
    "/", 
    response_model=List[schemas.CourseResponse],
    dependencies=[Depends(allow_view)]
)
def get_all(db: Session = Depends(get_db)):
    return crud.get_courses(db)


# ✅ VIEW ONE → STUDENT + FACULTY
@router.get(
    "/{course_id}", 
    response_model=schemas.CourseResponse,
    dependencies=[Depends(allow_view)]
)
def get_one(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course_by_id(db, course_id)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course


# ❌ UPDATE → ONLY FACULTY
@router.put(
    "/{course_id}", 
    response_model=schemas.CourseResponse,
    dependencies=[Depends(require_faculty)]
)
def update(course_id: int, course: schemas.CourseUpdate, db: Session = Depends(get_db)):
    updated = crud.update_course(db, course_id, course)

    if not updated:
        raise HTTPException(status_code=404, detail="Course not found")

    return updated


# ❌ PARTIAL UPDATE → ONLY FACULTY
@router.patch(
    "/{course_id}", 
    response_model=schemas.CourseResponse,
    dependencies=[Depends(require_faculty)]
)
def partial_update(course_id: int, course: schemas.CourseUpdate, db: Session = Depends(get_db)):
    updated = crud.update_course(db, course_id, course)

    if not updated:
        raise HTTPException(status_code=404, detail="Course not found")

    return updated


# ❌ DELETE → ONLY FACULTY
@router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_faculty)]
)
def delete(course_id: int, db: Session = Depends(get_db)):
    course = crud.delete_course(db, course_id)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return