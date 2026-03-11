from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User, Token
from app.services.auth import create_new_user, login


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register_user(user: User):
    try:
        response = create_new_user(user.email, user.password)
        return {"message": "User created successfully", "data": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        # OAuth2PasswordRequestForm uses 'username' field for the email
        response = login(form_data.username, form_data.password)

        if not response.session:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return {
            "access_token": response.session.access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
