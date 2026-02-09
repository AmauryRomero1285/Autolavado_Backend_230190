# pylint: disable=import-error, too-few-public-methods
'''
Vehicle Service Model Module.
Defines the SQLAlchemy model for the tbd_vehicle_services table.
'''
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from database.db import Base

class VehicleService(Base):
    '''
    Represents a vehicle service record in the database.
    '''
    __tablename__ = "tbd_vehicle_services"

    id = Column(Integer, primary_key=True, index=True)
    cashier_id = Column(Integer, ForeignKey("tbb_users.id"))
    cleaner_id = Column(Integer, ForeignKey("tbb_users.id"))
    service_id = Column(Integer, ForeignKey("tbc_services.id"))
    vehicle_id = Column(Integer, ForeignKey("tbb_vehicle.id"))
    service_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
