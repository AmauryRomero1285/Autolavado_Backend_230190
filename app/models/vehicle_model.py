# pylint: disable=import-error, too-few-public-methods
'''
Vehicle Model Module.
Defines the structure for the tbb_vehicle table.
'''
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from database.db import Base

class Vehicle(Base):
    '''
    Represents a vehicle entity in the database.
    '''
    __tablename__ = "tbb_vehicle"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("tbc_client.id"))
    license_plate = Column(String(60))
    model = Column(String(60))
    color = Column(String(60))
    owner_phone = Column(String(60))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
