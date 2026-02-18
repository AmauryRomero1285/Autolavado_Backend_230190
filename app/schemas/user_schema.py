'''Docstring for schema.user_schema'''
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    '''Clase para modelar los campos de tabla Usuarios'''
    first_name: str
    last_name: str
    second_last_name: str
    username:str
    password:str
    address: str
    email: str
    phone_number: str
    is_active:bool
    created_at: datetime
    updated_at: datetime
# pylint: disable=too-few-public-methods, unnecessary-pass
class UserCreate(UserBase):
    '''Clase para crear un Usuario basado en la tabla Usuario'''
    pass
class UserUpdate(UserBase):
    '''Clase para actualizar un Usuario basado en la tabla Usuario'''
    pass

class User(UserBase):
    '''Clase para realizar operaciones por ID en tabla Usuario'''
    Id: int
    class Config:
        '''Utilizar el orm para ejecutar las funcionalidades'''
        orm_mode =True

class UserLogin(BaseModel):
    '''Clase para realizar login por numero de telefono o correo'''
    phone_number: Optional[str] = None
    email: Optional[str] = None
    password: str
