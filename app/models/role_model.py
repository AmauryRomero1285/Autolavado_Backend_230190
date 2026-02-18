# pylint: disable=import-error, too-few-public-methods
'''
Role Model Module.
Defines the structure for the tbc_role table.
'''
from sqlalchemy import Column, Integer, String, Boolean,DateTime, func
from database.db import Base

class Role(Base):
    '''
    Represents a role entity in the database.
    '''
    __tablename__ = "tbc_role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at= Column(DateTime, onupdate=func.now())
