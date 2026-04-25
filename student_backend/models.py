from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

Date_of_Birth = Column(Date)

# ------------Department--------------
class Department(Base):
    __tablename__ = "Department"

    Dept_ID = Column(Integer, primary_key=True, index=True)
    Dept_Name = Column(String(100), unique=True, nullable=False)
    HOD_Name = Column(String(100))
    Location = Column(String(100))
    
# ---------------- STUDENT ----------------
class Student(Base):
    __tablename__ = "Student"

    Student_ID = Column(Integer, primary_key=True, index=True)
    FirstName = Column(String(50), nullable=False)
    LastName = Column(String(50), nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    Phone_no = Column(String(15))
    Address = Column(String(255))
    Date_of_Birth = Column(Date)
    EnrollmentYear = Column(Integer)
    Dept_ID = Column(Integer, ForeignKey("Department.Dept_ID"))

    enrollments = relationship("Enrollment", back_populates="student")

# ---------------- COURSE ----------------
class Course(Base):
    __tablename__ = "Course"

    Course_ID = Column(Integer, primary_key=True)
    Course_Name = Column(String(100))
    Credits = Column(Integer, nullable=False)
    Semester = Column(Integer)
    Course_Type = Column(String(20), nullable=False)
    Faculty_ID = Column(Integer)

    subjects = relationship("Subject", back_populates="course")  # ✅ keep this


# ---------------- SUBJECT ----------------
class Subject(Base):
    __tablename__ = "Subject"

    Subject_ID = Column(Integer, primary_key=True)
    Name = Column(String(100))
    Credits = Column(Integer)
    Course_ID = Column(Integer, ForeignKey("Course.Course_ID"))
    Semester = Column(Integer)

    course = relationship("Course", back_populates="subjects")

    # ✅ THIS LINE FIXES YOUR ERROR
    enrollments = relationship("Enrollment", back_populates="subject")


# ---------------- ENROLLMENT ----------------
class Enrollment(Base):
    __tablename__ = "enrollments"   # ✅ match DB exactly

    id = Column(Integer, primary_key=True, index=True)  # ✅ match DB

    student_id = Column(Integer, ForeignKey("Student.Student_ID"))
    subject_id = Column(Integer, ForeignKey("Subject.Subject_ID"))

    student = relationship("Student", back_populates="enrollments")
    subject = relationship("Subject", back_populates="enrollments")


# ---------------- MARKS ----------------
class Marks(Base):
    __tablename__ = "Marks"

    id = Column(Integer, primary_key=True)
    Student_ID = Column(Integer, ForeignKey("Student.Student_ID"))
    Subject_ID = Column(Integer, ForeignKey("Subject.Subject_ID"))

    Internal = Column(Float)
    External = Column(Float)
    Total = Column(Float)

    Grade = Column(String(2))
    
