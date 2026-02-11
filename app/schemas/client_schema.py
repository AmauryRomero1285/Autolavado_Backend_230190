'''Docstring for schema.client_schema'''
from typing import Optional
from pydantic import BaseModel

class ClientBase(BaseModel):
    ''' Clase para modelar los campos de tabla Clients'''
    nombre: str
    telefono: str
    estatus: bool

class ClientCreate(ClientBase):
    ''' Clase para crear un Cliente '''
    pass

class ClientUpdate(ClientBase):
    ''' Clase para actualizar un Cliente '''
    pass

class Client(ClientBase):
    ''' Clase para realizar operaciones por ID '''
    id: int
    class Config:
        orm_mode = True

