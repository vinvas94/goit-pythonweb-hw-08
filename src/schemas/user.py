from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=6, max_length=128)


class UserResponse(UserBase):
    id: int
    is_verified: bool = False
    avatar: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
