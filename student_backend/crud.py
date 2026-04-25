from sqlalchemy.orm import Session
import models, utils

# Student
def create_student(db: Session, student):
    try:
        # ✅ Check if email already exists
        existing = db.query(models.Student).filter(
            models.Student.Email == student.Email
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

        # ✅ Create student
        db_student = models.Student(**student.dict())

        db.add(db_student)
        db.commit()
        db.refresh(db_student)

        return db_student   # ✅ return created object

    except Exception as e:
        db.rollback()   # ✅ VERY IMPORTANT (avoid broken session)
        raise HTTPException(status_code=500, detail=str(e))
    
def update_student(db: Session, student_id: int, student_data):
    student = db.query(models.Student).filter(
        models.Student.Student_ID == student_id
    ).first()

    if not student:
        return None

    # ✅ prevent duplicate email
    if student_data.Email:
        existing = db.query(models.Student).filter(
            models.Student.Email == student_data.Email,
            models.Student.Student_ID != student_id
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

    # ✅ update only provided fields
    for key, value in student_data.dict(exclude_unset=True).items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student

def get_students(db: Session):
    return db.query(models.Student).all()

def get_student_by_id(db: Session, student_id: int):
    return db.query(models.Student).filter(
        models.Student.Student_ID == student_id
    ).first()


def delete_student(db: Session, student_id: int):
    student = db.query(models.Student).filter(
        models.Student.Student_ID == student_id
    ).first()

    if student:
        db.delete(student)
        db.commit()

    return student

# Course
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
    total = marks.internal + marks.external
    grade = utils.calculate_grade(total)

    db_marks = models.Marks(
        student_id=marks.student_id,
        subject_id=marks.subject_id,
        internal=marks.internal,
        external=marks.external,
        total=total,
        grade=grade
    )

    db.add(db_marks)
    db.commit()
    return db_marks


def get_student_result(db: Session, student_id: int):
    marks = db.query(models.Marks).filter(models.Marks.student_id == student_id).all()
    gpa = utils.calculate_gpa(marks)

    return {
        "marks": marks,
        "gpa": gpa,
        "status": "PASS" if gpa >= 5 else "FAIL"
    }