# schemas/service.py
"""
Esquemas Pydantic para la entidad Service en la API de autolavado.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import datetime


class ServiceBase(BaseModel):
    """Campos comunes seguros para lectura y base de otros esquemas"""
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    duration_minutes: int = Field(..., ge=5, le=240)  # duración en minutos, rango razonable


class ServiceCreate(ServiceBase):
    """POST /services – solo administradores o empleados con permiso"""
    pass


class ServiceUpdate(BaseModel):
    """PATCH /services/{id} – actualización parcial"""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    duration_minutes: Optional[int] = Field(None, ge=5, le=240)


class ServiceRead(ServiceBase):
    """Respuesta completa y segura"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={Decimal: str}
    )

class ServiceMinimal(BaseModel):
    id: int
    name: str
    price: Decimal
    duration_minutes: int

    model_config = ConfigDict(from_attributes=True)