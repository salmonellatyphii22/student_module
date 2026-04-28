from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import crud
from schemas import ReportCreate, ReportUpdate
from dependencies import require_faculty

router = APIRouter(prefix="/report", tags=["Faculty Report"])


# ➕ CREATE REPORT
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_report(
    data: ReportCreate,
    db: Session = Depends(get_db),
    user = Depends(require_faculty)
):
    return crud.create_report(db, data.dict())


# 📊 VIEW ALL REPORTS (FACULTY)
@router.get("/")
def get_all_reports(
    db: Session = Depends(get_db),
    user = Depends(require_faculty)
):
    reports = crud.get_all_reports(db)

    if not reports:
        return []

    return reports


# 🔍 VIEW ONE REPORT
@router.get("/{report_id}")
def get_one_report(
    report_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_faculty)
):
    report = crud.get_report_by_id(db, report_id)

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return report


# ✏️ UPDATE REPORT
@router.put("/{report_id}")
def update_report(
    report_id: int,
    data: ReportUpdate,
    db: Session = Depends(get_db),
    user = Depends(require_faculty)
):
    updated = crud.update_report(db, report_id, data.dict(exclude_unset=True))

    if not updated:
        raise HTTPException(status_code=404, detail="Report not found")

    return updated


# ❌ DELETE REPORT
@router.delete("/{report_id}", status_code=status.HTTP_200_OK)
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_faculty)
):
    deleted = crud.delete_report(db, report_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Report not found")

    return {"message": "Report deleted successfully"}