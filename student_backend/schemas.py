from pydantic import BaseModel
from datetime import date
from typing import Optional


# ---------------- STUDENT ----------------
class StudentBase(BaseModel):
    FirstName: str
    LastName: str
    Email: str
    Phone_no: str
    Address: str
    EnrollmentYear: int
    Dept_ID: int
    Date_of_Birth: date


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    Email: Optional[str] = None
    Phone_no: Optional[str] = None
    Address: Optional[str] = None
    EnrollmentYear: Optional[int] = None
    Dept_ID: Optional[int] = None
    Date_of_Birth: Optional[date] = None


class StudentResponse(StudentBase):
    Student_ID: int

    class Config:
        from_attributes = True
        

# ---------------- COURSE ----------------

class CourseBase(BaseModel):
    Course_Name: str
    Credits: int
    Course_Type: str
    Semester: Optional[int] = None
    Faculty_ID: Optional[int] = None


class CourseCreate(CourseBase):
    Course_ID: int   # only if manually provided


class CourseUpdate(BaseModel):
    Course_Name: Optional[str] = None
    Credits: Optional[int] = None
    Course_Type: Optional[str] = None
    Semester: Optional[int] = None
    Faculty_ID: Optional[int] = None


class CourseResponse(CourseBase):
    Course_ID: int

    class Config:
        from_attributes = True


# ---------------- SUBJECT ----------------
class SubjectBase(BaseModel):
    Name: str
    Credits: int
    Course_ID: int
    Semester: int


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    Name: Optional[str] = None
    Credits: Optional[int] = None
    Course_ID: Optional[int] = None
    Semester: Optional[int] = None


class SubjectResponse(SubjectBase):
    Subject_ID: int

    class Config:
        from_attributes = True


# ---------------- ENROLLMENT ----------------
class EnrollmentCreate(BaseModel):
    student_id: int
    subject_id: int


# ---------------- MARKS ----------------
class MarksCreate(BaseModel):
    Student_ID: int
    Subject_ID: int
    Internal: float
    External: float
    
class DepartmentBase(BaseModel):
    Dept_Name: str
    HOD_Name: Optional[str] = None
    Location: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    Dept_Name: Optional[str] = None
    HOD_Name: Optional[str] = None
    Location: Optional[str] = None


class DepartmentResponse(DepartmentBase):
    Dept_ID: int

    class Config:
        from_attributes = True
        
class FacultyBase(BaseModel):
    Name: str
    Email: str
    Phone_no: Optional[str] = None
    Designation: Optional[str] = None
    Salary: Optional[float] = None
    Dept_ID: int


class FacultyCreate(FacultyBase):
    pass


class FacultyUpdate(BaseModel):
    Name: Optional[str] = None
    Email: Optional[str] = None
    Phone_no: Optional[str] = None
    Designation: Optional[str] = None
    Salary: Optional[float] = None
    Dept_ID: Optional[int] = None


class FacultyResponse(FacultyBase):
    Faculty_ID: int

    class Config:
        from_attributes = True
        
# ---------------- EXAM ----------------

class ExamBase(BaseModel):
    Exam_Type: str
    Exam_Date: date
    Total_Marks: int
    Faculty_ID: int


class ExamCreate(ExamBase):
    pass


class ExamUpdate(BaseModel):
    Exam_Type: Optional[str] = None
    Exam_Date: Optional[date] = None
    Total_Marks: Optional[int] = None
    Faculty_ID: Optional[int] = None


class ExamResponse(ExamBase):
    Exam_ID: int

    class Config:
        from_attributes = True