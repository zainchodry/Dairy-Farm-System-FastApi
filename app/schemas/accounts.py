from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import date, datetime
from models.accounts import RoleEnum

class ProfileBase(BaseModel):
    phone_number: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None

class ProfileResponse(ProfileBase):
    id: int
    hire_date: datetime
    is_active_employee: bool
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    role: RoleEnum
    profile: Optional[ProfileResponse]
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
