from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Validates the Google OAuth JWT Token.
    For this POC, we mock the validation.
    """
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # In a real system, you would use google.oauth2.id_token.verify_oauth2_token
    # Return a mocked admin or standard user based on token content
    return {
        "email": "portfolio.manager@sbecipher.com",
        "role": "ADMIN" if "admin" in token.lower() else "USER"
    }
