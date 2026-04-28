from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

# 🔐 Same key used in auth.py
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

security = HTTPBearer()


# ✅ Get current logged-in user
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

security = HTTPBearer()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")
        role = payload.get("role")

        # ✅ STRICT VALIDATION
        if not user_id or not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token data"
            )

        # ✅ RETURN CLEAN STRUCTURE
        return {
            "user_id": int(user_id),   # ensure int
            "role": role
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


# 🔒 Only Faculty/Admin can modify
def require_student(user=Depends(get_current_user)):
    print("USER DEBUG:", user)


def require_faculty(user = Depends(get_current_user)):
    if user["role"] not in ["Faculty", "Admin"]:
        raise HTTPException(status_code=403, detail="Faculty/Admin only")
    return user


def allow_view(user = Depends(get_current_user)):
    if user["role"] not in ["Student", "Faculty", "Admin"]:
        raise HTTPException(status_code=403)
    return user