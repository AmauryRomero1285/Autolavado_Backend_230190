'''Docstring for schema.vehicle_schema'''
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class VehicleBase(BaseModel):
    ''' Clase para modelar los campos de tabla Vehicles'''
    placa: str
    marca: str
    modelo: str
    color: str
    tipo:str
    anio: str
    is_active:bool
    created_at:datetime
    updated_at:datetime

class VehicleCreate(VehicleBase):
    ''' Clase para crear un Vehiculo '''
    pass

class VehicleUpdate(VehicleBase):
    ''' Clase para actualizar un Vehiculo '''
    pass

class Vehicle(VehicleBase):
    ''' Clase para realizar operaciones por ID '''
    id: int
    class Config:
        orm_mode = True
