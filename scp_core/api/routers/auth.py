from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Any, Dict
from scp_core.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])

class AuthPayload(BaseModel):
    credential: str

@router.post("/google")
def authenticate_google(payload: AuthPayload):
    """
    Exchanges a Google OAuth credential for a session or JWT.
    """
    # For POC, we simulate reading the role from the email or database.
    role = "ADMIN" if "admin" in payload.credential.lower() else "USER"
    return {
        "status": "SUCCESS",
        "token": payload.credential,
        "user": {
            "email": "user@sbecipher.com",
            "role": role,
            "name": "Sbecipher User"
        }
    }

@router.get("/me")
def get_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    return current_user
