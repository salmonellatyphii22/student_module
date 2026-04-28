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


# ✅ LOGIN SCHEMA
class LoginRequest(BaseModel):
    username: str
    password: str


# ✅ SIGNUP SCHEMA (UPDATED)
class SignupRequest(BaseModel):
    username: str
    password: str
    role: str = "Student"   # default role


# 🔐 HASH PASSWORD
def get_password_hash(password: str):
    return pwd_context.hash(password)


# 🔐 VERIFY PASSWORD
def verify_password(plain, hashed):
    try:
        return pwd_context.verify(plain, hashed)
    except Exception:
        return False


# ✅ LOGIN API
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(models.Authentication_System).filter(
        models.Authentication_System.Username == data.username
    ).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not verify_password(data.password, user.Password):
        raise HTTPException(status_code=401, detail="Invalid password")

    # ✅ Ensure valid user_id (NO NULL EVER)
    user_id = user.User_ID if user.User_ID else user.Login_ID

    if not user_id:
        raise HTTPException(status_code=500, detail="User ID missing in database")

    # ✅ Create JWT payload
    payload = {
        "user_id": int(user_id),   # force integer
        "role": user.Role,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.Role,
        "user_id": int(user_id)   # optional but useful for frontend
    }


# ✅ SIGNUP API
@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):

    existing_user = db.query(models.Authentication_System).filter(
        models.Authentication_System.Username == data.username
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(data.password)

    # Step 1: create user WITHOUT User_ID
    new_user = models.Authentication_System(
        Username=data.username,
        Password=hashed_password,
        Role=data.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Step 2: assign User_ID = Login_ID ✅
    new_user.User_ID = new_user.Login_ID

    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}