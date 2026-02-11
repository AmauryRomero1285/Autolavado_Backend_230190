'''Docstring for schema.vehicle_services_schema'''
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class VehicleServiceBase(BaseModel):
    ''' Clase para modelar la relación entre vehiculos y servicios '''
    vehicle_id: int
    service_id: int
    fecha_servicio: datetime
    observaciones: Optional[str] = None

class VehicleServiceCreate(VehicleServiceBase):
    ''' Clase para registrar un nuevo servicio a un vehiculo '''
    pass

class VehicleServiceUpdate(VehicleServiceBase):
    ''' Clase para actualizar el registro del servicio '''
    pass

class VehicleService(VehicleServiceBase):
    ''' Clase para realizar operaciones por ID '''
    id: int
    class Config:
        orm_mode = True
