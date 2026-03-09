# models/inventary_movement.py
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum, func
from db import Base
import enum

class MovementType(enum.Enum):
    IN = "IN"
    OUT = "OUT"

class InventaryMovement(Base):
    __tablename__ = "inventory_movements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity = Column(Numeric(10, 2), nullable=False)
    type = Column(Enum(MovementType), nullable=False)
    reason = Column(String(50), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
