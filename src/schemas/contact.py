from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class ContactSchema(BaseModel):
    first_name: str = Field(min_length=2, max_length=50, description="First name of the contact")
    last_name: str = Field(min_length=2, max_length=50, description="Last name of the contact")
    email: EmailStr = Field(description="Email address of the contact")
    phone: str = Field(min_length=6, max_length=20, description="Phone number")
    birthday: date = Field(description="Birthday of the contact")
    extra_info: Optional[str] = Field(default=None, max_length=255, description="Additional info")


class ContactUpdateSchema(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    email: Optional[EmailStr] = Field(default=None)
    phone: Optional[str] = Field(default=None, min_length=6, max_length=20)
    birthday: Optional[date] = Field(default=None)
    extra_info: Optional[str] = Field(default=None, max_length=255)


class ContactResponse(ContactSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
