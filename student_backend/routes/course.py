from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
from typing import List

router = APIRouter(prefix="/courses", tags=["Courses"])


# ✅ CREATE COURSE
@router.post("/", response_model=schemas.CourseResponse, status_code=status.HTTP_201_CREATED)
def create(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, course)


# ✅ GET ALL COURSES
@router.get("/", response_model=List[schemas.CourseResponse])
def get_all(db: Session = Depends(get_db)):
    return crud.get_courses(db)


# ✅ GET COURSE BY ID
@router.get("/{course_id}", response_model=schemas.CourseResponse)
def get_one(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course_by_id(db, course_id)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course


# ✅ UPDATE COURSE (PUT)
@router.put("/{course_id}", response_model=schemas.CourseResponse)
def update(course_id: int, course: schemas.CourseUpdate, db: Session = Depends(get_db)):
    updated = crud.update_course(db, course_id, course)

    if not updated:
        raise HTTPException(status_code=404, detail="Course not found")

    return updated


# ✅ PARTIAL UPDATE (PATCH)
@router.patch("/{course_id}", response_model=schemas.CourseResponse)
def partial_update(course_id: int, course: schemas.CourseUpdate, db: Session = Depends(get_db)):
    updated = crud.update_course(db, course_id, course)

    if not updated:
        raise HTTPException(status_code=404, detail="Course not found")

    return updated


# ✅ DELETE COURSE
@router.delete("/{course_id}")
def delete(course_id: int, db: Session = Depends(get_db)):
    course = crud.delete_course(db, course_id)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return {"message": "Course deleted successfully"}