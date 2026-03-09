# schemas/client.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.schemas.vehicle import VehicleMinimal


class ClientBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=60)
    last_name: str = Field(..., min_length=2, max_length=60)
    phone_number: str = Field(..., pattern=r"^\+?\d{10,15}$")
    email: Optional[EmailStr] = None


class ClientCreate(ClientBase):
    # password si el cliente tiene cuenta propia, o solo se crea desde admin/employee
    # En muchos lavados: el cliente puede registrarse o solo se crea al agendar cita
    pass


class ClientUpdate(BaseModel):
    first_name:str
    last_name: str
    phone_number: Optional[str] = Field(None, pattern=r"^\+?\d{10,15}$")
    email: EmailStr


class ClientRead(ClientBase):
    id: int
    is_active: bool
    vehicles: List[VehicleMinimal] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)