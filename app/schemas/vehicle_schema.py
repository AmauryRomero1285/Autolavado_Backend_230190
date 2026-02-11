'''Docstring for schema.vehicle_schema'''
from typing import Optional
from pydantic import BaseModel

class VehicleBase(BaseModel):
    ''' Clase para modelar los campos de tabla Vehicles'''
    placa: str
    marca: str
    modelo: str
    color: str
    client_id: int

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
