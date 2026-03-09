# schemas/vehicle.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class VehicleBase(BaseModel):
    license_plate: str = Field(..., pattern=r"^[A-Z0-9-]{5,10}$", description="Placa del vehículo (5-10 caracteres, mayúsculas, números y guiones)")
    brand: str = Field(..., min_length=2, max_length=50)
    model: str = Field(..., min_length=2, max_length=50)
    color: str = Field(..., min_length=3, max_length=30)
    vehicle_type: str = Field(..., description="Ej: Sedan, SUV, Pickup, Moto")
    year: int = Field(..., ge=1900, le=2030)


class VehicleCreate(VehicleBase):
    client_id: int = Field(..., gt=0, description="ID del cliente propietario")
    pass


class VehicleUpdate(BaseModel):
    license_plate: Optional[str] = Field(None, pattern=r"^[A-Z0-9-]{5,10}$")
    brand: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    vehicle_type: Optional[str] = None
    year: Optional[int] = Field(None, ge=1900, le=2030)


class VehicleRead(VehicleBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    # Opcional: owner: UserMinimal si se necesita relación

    model_config = ConfigDict(from_attributes=True)
    
class VehicleMinimal(BaseModel):
    id: int
    license_plate: str
    brand: str
    model: str
    color: str

    model_config = ConfigDict(from_attributes=True)