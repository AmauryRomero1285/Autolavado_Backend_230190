# pylint: disable=import-error, too-few-public-methods
'''
Role Model Module.
Defines the structure for the tbc_role table.
'''
from sqlalchemy import Column, Integer, String, Boolean
from database.db import Base

class Role(Base):
    '''
    Represents a role entity in the database.
    '''
    __tablename__ = "tbc_role"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(60))
    is_active = Column(Boolean, default=True)
