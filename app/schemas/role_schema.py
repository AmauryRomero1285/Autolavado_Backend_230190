# pylint: disable=too-few-public-methods
'''
Role Schema Module.
Defines Pydantic models for Role validation and serialization.
'''
from typing import Optional
from pydantic import BaseModel, ConfigDict

class RoleBase(BaseModel):
    '''
    Base schema for Role with common attributes.
    '''
    description: str
    is_active: bool = True

class RoleCreate(RoleBase):
    '''
    Schema for creating a new Role.
    '''
    pass

class RoleUpdate(BaseModel):
    '''
    Schema for updating an existing Role.
    '''
    description: Optional[str] = None
    is_active: Optional[bool] = None

class Role(RoleBase):
    '''
    Schema for Role response, including database fields.
    '''
    id: int
    
    model_config = ConfigDict(from_attributes=True)
