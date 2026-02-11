'''Docstring for schema.user_schema'''
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    ''' Clase para modelar los campos de tabla Users'''
    username: str
    email: EmailStr
    estatus: bool

class UserCreate(UserBase):
    ''' Clase para crear un Usuario '''
    password: str

class UserUpdate(UserBase):
    ''' Clase para actualizar un Usuario '''
    password: Optional[str] = None

class User(UserBase):
    ''' Clase para realizar operaciones por ID '''
    id: int
    class Config:
        orm_mode = True
