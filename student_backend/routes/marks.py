from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db

router = APIRouter()

@router.post("/")
def add_marks(data: schemas.MarksCreate, db: Session = Depends(get_db)):
    return crud.add_marks(db, data)