# schemas/user.py
from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict
from typing import Optional, Literal
from datetime import datetime
from app.schemas.role import RoleMinimal


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    second_last_name: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, pattern=r"^\+?\d{10,15}$")
    role_id: Optional[int] = None

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    second_last_name: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, pattern=r"^\+?\d{10,15}$")


class UserRead(UserBase):
    id: int
    email: str
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    second_last_name: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: bool
    role_id: int

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    identifier: str = Field(..., description="Puede ser email o número de teléfono")
    password: str = Field(..., min_length=1)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode='after')
    def normalize_identifier(self):
        return self


class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
