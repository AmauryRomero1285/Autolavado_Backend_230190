# schemas/inventary_movements.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import datetime
from enum import Enum

class MovementType(str, Enum):
    IN = "IN"
    OUT = "OUT"

class InventoryBase(BaseModel):
    product_id: int
    quantity: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    type: MovementType
    reason: Optional[str] = Field(None, max_length=50, examples=["Venta", "Compra", "Ajuste"])

class InventoryMinimal(InventoryBase):
    """Útil para listados rápidos"""
    pass

class InventoryCreate(InventoryBase):
    """Específico para la creación de un movimiento"""
    pass

class InventoryUpdate(BaseModel):
    """
    Nota: Los movimientos históricos no suelen editarse. 
    Se incluye por estructura, pero se recomienda cautela.
    """
    reason: Optional[str] = None
    is_active: Optional[bool] = None

class InventoryRead(InventoryBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
