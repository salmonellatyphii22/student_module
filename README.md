

# Student Module Management System

A backend-based Student Module Management System developed using **FastAPI, SQLAlchemy, and MySQL**. This project provides RESTful APIs for managing students, courses, subjects, enrollments, marks, and academic results.

## 🚀 Features

- Student Management – Create, retrieve, update, and delete student records.
- Course Management – Manage courses offered in the institution.
- Subject Management – Add and manage subjects associated with courses.
- Enrollment Management – Handle student course and subject enrollments.
- Marks Management – Store and manage student marks.
- Result Management – Manage and retrieve academic results.
- RESTful APIs – Structured and scalable API endpoints using FastAPI.
- Database Integration – Persistent data storage using MySQL and SQLAlchemy.
- Data Validation – Request and response validation using Pydantic schemas.

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend programming |
| FastAPI | REST API framework |
| SQLAlchemy | ORM and database interaction |
| MySQL | Relational database |
| Pydantic | Data validation |
| Uvicorn | ASGI server |

## 📂 Project Structure

```text
student_module/
│
├── database.py
├── models.py
├── schemas.py
├── main.py
│
├── routes/
│   ├── student.py
│   ├── course.py
│   ├── subject.py
│   ├── enrollment.py
│   ├── marks.py
│   └── result.py
│
├── requirements.txt
└── README.md
```

> Note: Update the project structure to match the actual files and folders in your repository.

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/salmonellatyphii22/student_module.git
```

Navigate to the project directory:

```bash
cd student_module
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

**macOS / Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Database

1. Install and start MySQL.
2. Create a database named `student_db`.
3. Update the database connection details in `database.py`.

Example:

```python
DATABASE_URL = "mysql+pymysql://username:password@localhost/student_db"
```

Replace `username` and `password` with your MySQL credentials.

### 5. Run the Application

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

## 📖 API Documentation

FastAPI provides interactive API documentation.

**Swagger UI:**

```text
http://127.0.0.1:8000/docs
```

**ReDoc:**

```text
http://127.0.0.1:8000/redoc
```

Use these interfaces to explore and test the available API endpoints.

## 🎯 Learning Outcomes

- Developed RESTful APIs using FastAPI.
- Implemented database operations using SQLAlchemy ORM.
- Integrated a MySQL relational database with a Python backend.
- Applied Pydantic models for data validation.
- Organized backend functionality using modular route files.
- Practiced CRUD operations and relational database management.

## 🔮 Future Enhancements

- User authentication and authorization.
- Role-based access for administrators and students.
- Student performance analytics.
- Pagination and advanced filtering.
- Frontend integration.
- Automated testing for API endpoints.

## 👩‍💻 Author

**Sweta Jha**

- GitHub: [salmonellatyphii22](https://github.com/salmonellatyphii22)

## 📄 License

This project is developed for educational and learning purposes.
