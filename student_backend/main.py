from fastapi import FastAPI
from database import engine, Base

from routes import student, course, subject, enrollment, marks, result

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
    allow_origins=["*"],  # change later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Include Routers (CLEAN PREFIXES)
# ==============================
app.include_router(student.router, prefix="/students", tags=["Students"])
app.include_router(course.router, prefix="/courses", tags=["Courses"])
app.include_router(subject.router, prefix="/subjects", tags=["Subjects"])
# app.include_router(enrollment.router, prefix="/enrollments", tags=["Enrollments"])
app.include_router(marks.router, prefix="/marks", tags=["Marks"])
app.include_router(result.router, prefix="/results", tags=["Results"])