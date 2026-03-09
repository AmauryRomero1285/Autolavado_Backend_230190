# models/service.py
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func
from db import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)     
    duration_minutes = Column(Integer, nullable=False) 
    is_active = Column(Boolean, nullable=False, server_default="true", default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())