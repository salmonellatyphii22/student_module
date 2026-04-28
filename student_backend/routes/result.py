from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import crud
from dependencies import require_student
from schemas import ReportResponse

from dependencies import allow_view

router = APIRouter(prefix="/result", tags=["Result"])
@router.get("/", response_model=List[ReportResponse])
def get_my_result(
    db: Session = Depends(get_db),
    user = Depends(allow_view)
):
    # 🔐 SAFETY CHECK
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 👇 STUDENT → OWN RESULT
    if user["role"] == "Student":
        student_id = user["user_id"]
        return crud.get_student_result(db, student_id)

    # 👇 FACULTY → ALL REPORTS
    elif user["role"] in ["Faculty", "Admin"]:
        return crud.get_all_reports(db)

    raise HTTPException(status_code=403, detail="Access denied")