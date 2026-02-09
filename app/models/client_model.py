# pylint: disable=import-error, too-few-public-methods
'''
Client Model Module.
Defines the structure for the tbc_client table.
'''
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database.db import Base

class Client(Base):
    '''
    Represents a client entity in the database.
    '''
    __tablename__ = "tbc_client"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60))
    last_name = Column(String(60))
    second_last_name = Column(String(60))
    address = Column(String(60))
    phone_number = Column(String(10))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
