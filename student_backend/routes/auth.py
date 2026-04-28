from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ✅ Request schema
class LoginRequest(BaseModel):
    username: str
    password: str


# 🔐 Hash password
def get_password_hash(password: str):
    return pwd_context.hash(password)


# 🔐 Verify password (SAFE VERSION)
def verify_password(plain, hashed):
    try:
        return pwd_context.verify(plain, hashed)
    except Exception:
        return False


# ❌ REMOVE THIS AFTER USE (IMPORTANT)
# @router.get("/generate-hash")
# def generate_hash():
#     return {"hash": get_password_hash("123")}


# ✅ LOGIN API
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(models.Authentication_System).filter(
        models.Authentication_System.Username == data.username
    ).first()

    # ✅ Better validation
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not verify_password(data.password, user.Password):
        raise HTTPException(status_code=401, detail="Invalid password")

    # 🎟️ Create JWT token
    payload = {
        "user_id": user.User_ID,
        "role": user.Role,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.Role
    }
    
# -------------------------
# SIGNUP API (ADD HERE)
# -------------------------
@router.post("/signup")
def signup(data: LoginRequest, db: Session = Depends(get_db)):

    # 🔍 Check if user already exists
    existing_user = db.query(models.Authentication_System).filter(
        models.Authentication_System.Username == data.username
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # 🔐 Hash password
    hashed_password = get_password_hash(data.password)

    # ✅ Create new user
    new_user = models.Authentication_System(
        Username=data.username,
        Password=hashed_password,
        Role="Student",
        User_ID=1
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}