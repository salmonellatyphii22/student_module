from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal

router = APIRouter(prefix="/report", tags=["Report"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{student_id}")
def report_card(student_id: int, db: Session = Depends(get_db)):
    result = db.execute("""
        SELECT c.Course_Name, ar.Marks_Obtained, ar.Grade, ar.Result_Status
        FROM Academic_Report ar
        JOIN Course c ON ar.Course_ID = c.Course_ID
        WHERE ar.Student_ID = :student_id
    """, {"student_id": student_id}).fetchall()

    return [dict(row._mapping) for row in result]