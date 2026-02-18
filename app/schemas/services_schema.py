'''Docstring for schema.services_schema'''
from datetime import datetime
from pydantic import BaseModel

class ServiceBase(BaseModel):
    ''' Clase para modelar los campos de tabla Services'''
    nombre_servicio: str
    descripcion: Optional[str] = None
    precio: float
    duración:int
    estatus: bool
    created_at: datetime
    updated_at: datetime

class ServiceCreate(ServiceBase):
    ''' Clase para crear un Servicio '''
    pass

class ServiceUpdate(ServiceBase):
    ''' Clase para actualizar un Servicio '''
    pass

class Service(ServiceBase):
    ''' Clase para realizar operaciones por ID '''
    id: int
    class Config:
        orm_mode = True
