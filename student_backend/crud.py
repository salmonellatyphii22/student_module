from sqlalchemy.orm import Session
import models, utils
from fastapi import HTTPException

# ---------------- CREATE STUDENT ----------------
def create_student(db: Session, student):
    try:
        existing = db.query(models.Student).filter(
            models.Student.Email == student.Email
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

        db_student = models.Student(**student.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)

        return db_student

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- UPDATE STUDENT ----------------
def update_student(db: Session, student_id: int, student_data):
    student = db.query(models.Student).filter(
        models.Student.Student_ID == student_id
    ).first()

    if not student:
        return None

    # Prevent duplicate email
    if student_data.Email:
        existing = db.query(models.Student).filter(
            models.Student.Email == student_data.Email,
            models.Student.Student_ID != student_id
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

    for key, value in student_data.dict(exclude_unset=True).items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student


# ---------------- GET ALL STUDENTS (WITH COURSES) ----------------
def get_students(db: Session):
    students = db.query(models.Student).all()
    result = []

    for student in students:
        enrollments = (
            db.query(models.Enrollment)
            .filter(models.Enrollment.Student_ID == student.Student_ID)
            .all()
        )

        course_data = []

        for enroll in enrollments:
            course = db.query(models.Course).filter(
                models.Course.Course_ID == enroll.Course_ID
            ).first()

            if course:
                course_data.append({
                    "Course_ID": course.Course_ID,
                    "Course_Name": course.Course_Name,
                    "Credits": course.Credits,
                    "Semester": enroll.Semester,
                    "Enrollment_Date": enroll.Enrollment_Date,
                    "Status": enroll.Status
                })

        result.append({
            "Student_ID": student.Student_ID,
            "FirstName": student.FirstName,
            "LastName": student.LastName,
            "Email": student.Email,
            "Phone_no": student.Phone_no,
            "Address": student.Address,
            "Date_of_Birth": student.Date_of_Birth,
            "EnrollmentYear": student.EnrollmentYear,
            "Dept_ID": student.Dept_ID,
            "Courses": course_data
        })

    return result


# ---------------- GET STUDENT BY ID (WITH COURSES) ----------------
def get_student_by_id(db: Session, student_id: int):
    student = db.query(models.Student).filter(
        models.Student.Student_ID == student_id
    ).first()

    if not student:
        return None

    enrollments = (
        db.query(models.Enrollment)
        .filter(models.Enrollment.Student_ID == student.Student_ID)
        .all()
    )

    course_data = []

    for enroll in enrollments:
        course = db.query(models.Course).filter(
            models.Course.Course_ID == enroll.Course_ID
        ).first()

        if course:
            course_data.append({
                "Course_ID": course.Course_ID,
                "Course_Name": course.Course_Name,
                "Credits": course.Credits,
                "Semester": enroll.Semester,
                "Enrollment_Date": enroll.Enrollment_Date,
                "Status": enroll.Status
            })

    return {
        "Student_ID": student.Student_ID,
        "FirstName": student.FirstName,
        "LastName": student.LastName,
        "Email": student.Email,
        "Phone_no": student.Phone_no,
        "Address": student.Address,
        "Date_of_Birth": student.Date_of_Birth,
        "EnrollmentYear": student.EnrollmentYear,
        "Dept_ID": student.Dept_ID,

        # ✅ COURSES INCLUDED
        "Courses": course_data
    }

# ---------------- DELETE STUDENT ----------------
def delete_student(db: Session, student_id: int):
    student = db.query(models.Student).filter(
        models.Student.Student_ID == student_id
    ).first()

    if student:
        db.delete(student)
        db.commit()

    return student

# -------------Course----------
def create_course(db, course):
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

# 🔹 GET ALL
def get_courses(db: Session):
    return db.query(models.Course).all()


# 🔹 GET BY ID
def get_course_by_id(db: Session, course_id: int):
    return db.query(models.Course).filter(
        models.Course.Course_ID == course_id
    ).first()


# 🔹 UPDATE
def update_course(db: Session, course_id: int, course_data):
    course = db.query(models.Course).filter(
        models.Course.Course_ID == course_id
    ).first()

    if not course:
        return None

    for key, value in course_data.dict(exclude_unset=True).items():
        setattr(course, key, value)

    db.commit()
    db.refresh(course)

    return course


# 🔹 DELETE
def delete_course(db: Session, course_id: int):
    course = db.query(models.Course).filter(
        models.Course.Course_ID == course_id
    ).first()

    if course:
        db.delete(course)
        db.commit()

    return course


# Subject
def create_subject(db: Session, subject):
    db_subject = models.Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    return db_subject

# 🔹 GET ALL SUBJECTS
def get_subjects(db: Session):
    return db.query(models.Subject).all()


# 🔹 GET SUBJECT BY ID
def get_subject_by_id(db: Session, subject_id: int):
    return db.query(models.Subject).filter(
        models.Subject.Subject_ID == subject_id
    ).first()


# 🔹 UPDATE SUBJECT
def update_subject(db: Session, subject_id: int, subject_data):
    subject = db.query(models.Subject).filter(
        models.Subject.Subject_ID == subject_id
    ).first()

    if not subject:
        return None

    for key, value in subject_data.dict(exclude_unset=True).items():
        setattr(subject, key, value)

    db.commit()
    db.refresh(subject)

    return subject


# 🔹 DELETE SUBJECT
def delete_subject(db: Session, subject_id: int):
    subject = db.query(models.Subject).filter(
        models.Subject.Subject_ID == subject_id
    ).first()

    if subject:
        db.delete(subject)
        db.commit()

    return subject


# Enrollment
def enroll_student(db: Session, enroll):
    db_enroll = models.Enrollment(**enroll.dict())
    db.add(db_enroll)
    db.commit()
    return db_enroll


# Marks
def add_marks(db: Session, marks):
    total = marks.Internal + marks.External
    grade = utils.calculate_grade(total)

    db_marks = models.Marks(
        Student_ID=marks.Student_ID,
        Subject_ID=marks.Subject_ID,
        Internal=marks.Internal,
        External=marks.External,
        Total=total,
        Grade=grade
    )

    db.add(db_marks)
    db.commit()
    db.refresh(db_marks)
    return db_marks


def get_student_result(db: Session, student_id: int):
    marks = db.query(models.Marks).filter(models.Marks.student_id == student_id).all()
    gpa = utils.calculate_gpa(marks)

    return {
        "marks": marks,
        "gpa": gpa,
        "status": "PASS" if gpa >= 5 else "FAIL"
    }
    
# ---------------- FACULTY ----------------

def create_faculty(db: Session, faculty):
    db_faculty = models.Faculty(**faculty.dict())
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty


def get_faculties(db: Session):
    return db.query(models.Faculty).all()


def get_faculty_by_id(db: Session, faculty_id: int):
    return db.query(models.Faculty).filter(
        models.Faculty.Faculty_ID == faculty_id
    ).first()


def update_faculty(db: Session, faculty_id: int, faculty_data):
    faculty = get_faculty_by_id(db, faculty_id)

    if not faculty:
        return None

    for key, value in faculty_data.dict(exclude_unset=True).items():
        setattr(faculty, key, value)

    db.commit()
    db.refresh(faculty)
    return faculty


def delete_faculty(db: Session, faculty_id: int):
    faculty = get_faculty_by_id(db, faculty_id)

    if faculty:
        db.delete(faculty)
        db.commit()

    return faculty

# ---------------- DEPARTMENT ----------------

def create_department(db: Session, department):
    db_department = models.Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


def get_departments(db: Session):
    return db.query(models.Department).all()


def get_department_by_id(db: Session, dept_id: int):
    return db.query(models.Department).filter(
        models.Department.Dept_ID == dept_id
    ).first()


def update_department(db: Session, dept_id: int, department_data):
    department = get_department_by_id(db, dept_id)

    if not department:
        return None

    for key, value in department_data.dict(exclude_unset=True).items():
        setattr(department, key, value)

    db.commit()
    db.refresh(department)
    return department


def delete_department(db: Session, dept_id: int):
    department = get_department_by_id(db, dept_id)

    if department:
        db.delete(department)
        db.commit()

    return department

# ---------------- EXAMINATION ----------------

def create_exam(db: Session, exam):
    db_exam = models.Examination(**exam.dict())
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam


def get_exams(db: Session):
    return db.query(models.Examination).all()


def get_exam_by_id(db: Session, exam_id: int):
    return db.query(models.Examination).filter(
        models.Examination.Exam_ID == exam_id
    ).first()


def update_exam(db: Session, exam_id: int, exam_data):
    exam = get_exam_by_id(db, exam_id)

    if not exam:
        return None

    for key, value in exam_data.dict(exclude_unset=True).items():
        setattr(exam, key, value)

    db.commit()
    db.refresh(exam)
    return exam


def delete_exam(db: Session, exam_id: int):
    exam = get_exam_by_id(db, exam_id)

    if exam:
        db.delete(exam)
        db.commit()

    return exam