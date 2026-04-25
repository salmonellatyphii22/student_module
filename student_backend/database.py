from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ==============================
# Database Credentials
# ==============================
USERNAME = "root"
PASSWORD = "Nihal#2704$"
HOST = "localhost"
PORT = 3306
DATABASE = "student_db"

# ==============================
# Database URL
# ==============================
DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# ==============================
# Engine
# ==============================
engine = create_engine(
    DATABASE_URL,
    echo=True,              # Debug logs (set False later)
    pool_pre_ping=True      # Fix MySQL connection timeout issue
)

# ==============================
# Session
# ==============================
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# ==============================
# Base Class
# ==============================
Base = declarative_base()

# ==============================
# Dependency (IMPORTANT)
# ==============================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()