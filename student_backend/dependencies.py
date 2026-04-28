from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

# 🔐 Same key used in auth.py
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

# 🔐 This enables Authorization: Bearer <token>
security = HTTPBearer()


# ✅ Get current logged-in user from token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload   # contains user_id + role
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# 🔒 Only Faculty/Admin can modify
def require_faculty(user=Depends(get_current_user)):
    if user["role"] not in ["Faculty", "Admin"]:
        raise HTTPException(status_code=403, detail="Only faculty/admin allowed")
    return user


# 👁️ Any logged-in user can view
def allow_view(user=Depends(get_current_user)):
    return user


# ❌ Optional: only student endpoints
def require_student(user=Depends(get_current_user)):
    if user["role"] != "Student":
        raise HTTPException(status_code=403, detail="Only students allowed")
    return user