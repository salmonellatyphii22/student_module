from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# ------------ Department --------------
class Department(Base):
    __tablename__ = "Department"

    Dept_ID = Column(Integer, primary_key=True, index=True)
    Dept_Name = Column(String(100), unique=True, nullable=False)
    HOD_Name = Column(String(100))
    Location = Column(String(100))

    # ✅ Relationships
    students = relationship("Student", back_populates="department")
    faculty = relationship("Faculty", back_populates="department")


# ---------------- FACULTY ----------------
class Faculty(Base):
    __tablename__ = "Faculty"

    Faculty_ID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    Phone_no = Column(String(15))
    Designation = Column(String(50))
    Salary = Column(Float)

    Dept_ID = Column(Integer, ForeignKey("Department.Dept_ID"))

    # ✅ Relationships
    department = relationship("Department", back_populates="faculty")
    courses = relationship("Course", back_populates="faculty")


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

    # ✅ Relationships
    department = relationship("Department", back_populates="students")

    # 👉 IMPORTANT: cascade helps in deletion
    enrollments = relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete"
    )


# ---------------- COURSE ----------------
class Course(Base):
    __tablename__ = "Course"

    Course_ID = Column(Integer, primary_key=True)
    Course_Name = Column(String(100))
    Credits = Column(Integer, nullable=False)
    Semester = Column(Integer)
    Course_Type = Column(String(20), nullable=False)

    Faculty_ID = Column(Integer, ForeignKey("Faculty.Faculty_ID"))

    # ✅ Relationships
    subjects = relationship("Subject", back_populates="course")
    faculty = relationship("Faculty", back_populates="courses")


# ---------------- SUBJECT ----------------
class Subject(Base):
    __tablename__ = "Subject"

    Subject_ID = Column(Integer, primary_key=True)
    Name = Column(String(100))
    Credits = Column(Integer)
    Course_ID = Column(Integer, ForeignKey("Course.Course_ID"))
    Semester = Column(Integer)

    course = relationship("Course", back_populates="subjects")


# ---------------- ENROLLMENT ----------------
class Enrollment(Base):
    __tablename__ = "Enrollment"

    Student_ID = Column(Integer, ForeignKey("Student.Student_ID"), primary_key=True)
    Course_ID = Column(Integer, ForeignKey("Course.Course_ID"), primary_key=True)

    Enrollment_Date = Column(Date, nullable=False)
    Semester = Column(Integer)
    Status = Column(String(20))

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course")


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
    
class Examination(Base):
    __tablename__ = "Examination"

    Exam_ID = Column(Integer, primary_key=True, index=True)
    Exam_Type = Column(String(50))
    Exam_Date = Column(Date)
    Total_Marks = Column(Integer)
    Faculty_ID = Column(Integer, ForeignKey("Faculty.Faculty_ID"))
    
# ---------------- AUTH ----------------
class Authentication_System(Base):
    __tablename__ = "Authentication_System"

    Login_ID = Column(Integer, primary_key=True, index=True)
    Username = Column(String(100), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)  # store HASHED password
    Role = Column(String(20), nullable=False)       # Student / Faculty / Admin
    User_ID = Column(Integer, nullable=False)       # FK to Student_ID or Faculty_ID