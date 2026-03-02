# models/client.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, unique=True, index=True)  # relación opcional con usuario registrado
    
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    phone_number = Column(String(20), nullable=False, index=True, unique=True)
    email = Column(String(120), nullable=True, index=True)
    notes = Column(String(500), nullable=True)
    
    is_active = Column(Boolean, nullable=False, server_default="true", default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    vehicles = relationship("Vehicle", back_populates="client", cascade="all, delete-orphan")
    
    # Si quieres:
    appointments = relationship("Appointment", back_populates="client")