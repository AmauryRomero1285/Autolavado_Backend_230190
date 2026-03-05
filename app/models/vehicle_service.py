from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from db import Base

class VehicleService(Base):
    __tablename__ = "vehiculo_servicio"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="RESTRICT"), nullable=False)
    
    employee_casher_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    employee_washer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    status = Column(String(30), nullable=False, default="pendiente")
    scheduled_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    
    # Nuevas columnas de precios
    service_price = Column(DECIMAL(10, 2), nullable=True)
    discount = Column(DECIMAL(10, 2), default=0.00)
    total_price = Column(DECIMAL(10, 2), nullable=True)
    
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    vehicle = relationship("Vehicle")
    service = relationship("Service")
    casher = relationship("User", foreign_keys=[employee_casher_id])
    washer = relationship("User", foreign_keys=[employee_washer_id])
