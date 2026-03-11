from pydantic import BaseModel, Field


class User(BaseModel):
    email: str
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    id: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
