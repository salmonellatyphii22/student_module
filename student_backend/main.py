from fastapi import FastAPI
from database import engine, Base

from routes import student, course, subject, enrollment, marks, result
from routes import faculty, department, exam, auth   # ✅ ADD auth

from fastapi.middleware.cors import CORSMiddleware

# ==============================
# App Initialization
# ==============================
app = FastAPI()

# ==============================
# Create Tables
# ==============================
Base.metadata.create_all(bind=engine)

# ==============================
# CORS (VERY IMPORTANT for frontend)
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Include Routers
# ==============================
app.include_router(auth.router)   # 🔥 VERY IMPORTANT (LOGIN)

app.include_router(student.router)
app.include_router(course.router)
app.include_router(subject.router)
# app.include_router(enrollment.router)
app.include_router(marks.router)
app.include_router(result.router)

app.include_router(faculty.router)
app.include_router(department.router)
app.include_router(exam.router)