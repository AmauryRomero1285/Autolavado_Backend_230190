'''
Docstring for schemas.schema_rol
'''
from pydantic import BaseModel
from datetime import datetime

class RoleBase(BaseModel):
    '''Clase para modelar los campos de tabla Role'''
    name:str
    is_active: bool
    created_at: datetime
    updated_at: datetime
# pylint: disable=too-few-public-methods, unnecessary-pass
class RolCreate(RoleBase):
    '''Clase para crear un Rol basado en la tabla Role'''
    pass
class RoleUpdate(RoleBase):
    '''Clase para actualizar un Rol basado en la tabla Role'''
    pass

class Role(RoleBase):
    '''Clase para realizar operaciones por ID en tabla Role'''
    Id: int
    class Config:
        '''Utilizar el orm para ejecutar las funcionalidades'''
        orm_mode =True
