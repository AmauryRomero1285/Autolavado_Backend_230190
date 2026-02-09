# pylint: disable=too-few-public-methods
'''
User Schema Module.
Defines Pydantic models for User validation and serialization.
'''
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class UserBase(BaseModel):
    '''
    Base schema for User with common attributes.
    '''
    role_id: int
    first_name: str
    last_name: str
    second_last_name: Optional[str] = None
    username: str
    phone_number: Optional[str] = Field(None, max_length=10)
    is_active: bool = True

class UserCreate(UserBase):
    '''
    Schema for creating a new User, including the password.
    '''
    password: str

class UserUpdate(BaseModel):
    '''
    Schema for updating an existing User. All fields are optional.
    '''
    role_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    second_last_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    '''
    Schema for User response, including database fields and timestamps.
    '''
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
