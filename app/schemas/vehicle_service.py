from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from decimal import Decimal

class VehicleServiceBase(BaseModel):
    vehicle_id: int
    service_id: int
    employee_casher_id: Optional[int] = None
    employee_washer_id: Optional[int] = None
    status: str = "pendiente"
    scheduled_at: Optional[datetime] = None
    service_price: Optional[Decimal] = None
    discount: Optional[Decimal] = Decimal("0.00")
    total_price: Optional[Decimal] = None
    notes: Optional[str] = None

class VehicleServiceCreate(VehicleServiceBase):
    pass

class VehicleServiceUpdate(BaseModel):
    status: Optional[str] = None
    employee_washer_id: Optional[int] = None 
    employee_casher_id: Optional[int] = None 
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    service_price: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    total_price: Optional[Decimal] = None
    notes: Optional[str] = None

class VehicleServiceRead(VehicleServiceBase):
    id: int
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
