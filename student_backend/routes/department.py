from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
from typing import List
from dependencies import require_faculty, allow_view

router = APIRouter(prefix="/department", tags=["Department"])


# ❌ CREATE → ONLY FACULTY
@router.post(
    "/", 
    response_model=schemas.DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_faculty)]
)
def create(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db, department)


# ✅ VIEW ALL → STUDENT + FACULTY
@router.get(
    "/", 
    response_model=List[schemas.DepartmentResponse],
    dependencies=[Depends(allow_view)]
)
def get_all(db: Session = Depends(get_db)):
    return crud.get_departments(db)


# ✅ VIEW ONE → STUDENT + FACULTY
@router.get(
    "/{Dept_ID}", 
    response_model=schemas.DepartmentResponse,
    dependencies=[Depends(allow_view)]
)
def get_one(Dept_ID: int, db: Session = Depends(get_db)):
    department = crud.get_department_by_id(db, Dept_ID)

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    return department


# ❌ UPDATE → ONLY FACULTY
@router.put(
    "/{Dept_ID}", 
    response_model=schemas.DepartmentResponse,
    dependencies=[Depends(require_faculty)]
)
def update(Dept_ID: int, department: schemas.DepartmentUpdate, db: Session = Depends(get_db)):
    updated = crud.update_department(db, Dept_ID, department)

    if not updated:
        raise HTTPException(status_code=404, detail="Department not found")

    return updated


# ❌ PARTIAL UPDATE → ONLY FACULTY
@router.patch(
    "/{Dept_ID}", 
    response_model=schemas.DepartmentResponse,
    dependencies=[Depends(require_faculty)]
)
def partial_update(Dept_ID: int, department: schemas.DepartmentUpdate, db: Session = Depends(get_db)):
    updated = crud.update_department(db, Dept_ID, department)

    if not updated:
        raise HTTPException(status_code=404, detail="Department not found")

    return updated


# ❌ DELETE → ONLY FACULTY
@router.delete(
    "/{Dept_ID}", 
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_faculty)]
)
def delete(Dept_ID: int, db: Session = Depends(get_db)):
    department = crud.delete_department(db, Dept_ID)

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    return