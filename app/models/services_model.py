# pylint: disable=import-error, too-few-public-methods
'''
Services Model Module.
Defines the structure for the tbc_services table.
'''
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database.db import Base

class Service(Base):
    '''
    Represents a services entity in the database.
    '''
    __tablename__ = "tbc_services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60))
    description = Column(String(60))
    price = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
