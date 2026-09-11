"""
InsightBI AI — Auth Endpoints (backend/app/api/v1/auth.py)
Includes JWT login, registration, refresh tokens, and security audit logging.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import timedelta
from backend.app.schemas.auth import UserCreate, UserLogin, Token, UserResponse
from backend.app.core.security import hash_password, verify_password, create_access_token, decode_access_token, get_current_user
from backend.app.core.audit import log_security_event

router = APIRouter()

MOCK_USERS_DB = {}

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    if user.email in MOCK_USERS_DB:
        log_security_event("user_register", user.email, "FAILED", {"reason": "Email exists"})
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = hash_password(user.password)
    user_id = len(MOCK_USERS_DB) + 1
    user_record = {
        "id": user_id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "hashed_password": hashed_pwd,
        "is_active": True
    }
    MOCK_USERS_DB[user.email] = user_record
    log_security_event("user_register", user.email, "SUCCESS", {"role": user.role})
    return user_record

@router.post("/login", response_model=Token)
def login(credentials: UserLogin):
    user = MOCK_USERS_DB.get(credentials.email)
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        log_security_event("user_login", credentials.email, "FAILED", {"reason": "Invalid credentials"})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    token = create_access_token({"sub": user["email"], "role": user["role"]})
    log_security_event("user_login", credentials.email, "SUCCESS", {"role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
def refresh_token(request: RefreshTokenRequest):
    payload = decode_access_token(request.refresh_token)
    email = payload.get("sub")
    role = payload.get("role", "Analyst")
    new_token = create_access_token({"sub": email, "role": role}, expires_delta=timedelta(hours=1))
    log_security_event("token_refresh", email, "SUCCESS")
    return {"access_token": new_token, "token_type": "bearer"}

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    email = current_user.get("sub")
    user = MOCK_USERS_DB.get(email, {"email": email, "role": current_user.get("role", "Analyst")})
    return {"email": user["email"], "role": user.get("role", "Analyst")}
