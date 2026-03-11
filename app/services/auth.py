from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.database import supabase

# tokenUrl must point to the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def create_new_user(email: str, password: str):
    try:
        data = supabase.auth.sign_up(
            {
                "email": email,
                "password": password
            }
        )
        return data
    except Exception as e:
        raise e


def login(email: str, password: str):
    try:
        data = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )
        return data
    except Exception as e:
        raise e


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # The oauth2_scheme returns the token string directly
        user = supabase.auth.get_user(token)
        if not user or not user.user:
            raise HTTPException(
                status_code=401,
                detail="Invalid token or user not found"
            )
        return user.user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
