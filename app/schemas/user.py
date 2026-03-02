# schemas/user.py
from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict
from typing import Optional,Literal
from datetime import datetime
from app.schemas.role import RoleMinimal


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone_number: Optional[str] = Field(None, pattern=r"^\+?\d{10,15}$")


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, pattern=r"^\+?\d{10,15}$")


class UserRead(UserBase):
    id: int
    phone_number: Optional[str] = None
    is_active: bool
    role: Optional[RoleMinimal] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    identifier: str = Field(..., description="Puede ser email o número de teléfono")
    password: str = Field(..., min_length=1)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode='after')
    def normalize_identifier(self):
        # Aquí puedes decidir si normalizar teléfono o validar formato
        # Pero la lógica de distinguir email/teléfono la puedes hacer en el servicio
        return self


class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"