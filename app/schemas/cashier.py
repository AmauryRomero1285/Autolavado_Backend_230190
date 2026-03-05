from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from decimal import Decimal
from typing import Optional

class CashierDetail(BaseModel):
    id: int
    # Empleados involucrados
    nombre_cajero: Optional[str] = Field(None, alias="nombre-cajero")
    nombre_lavador: Optional[str] = Field(None, alias="nombre-lavador")
    
    # Detalle del servicio y Desglose de Precios
    nombre_servicio: Optional[str] = Field(None, alias="nombre-servicio")
    descripcion: Optional[str] = Field(None)
    precio_base: Optional[Decimal] = Field(None, alias="service-price") # Precio original
    descuento: Optional[Decimal] = Field(None, alias="discount")        # Monto descontado
    total_pagar: Optional[Decimal] = Field(None, alias="total-price")   # Precio final
    status: Optional[str] = Field(None)
    
    # Tiempos y Fechas
    fecha_programada: Optional[datetime] = Field(None, alias="scheduled-at")
    hora_inicio: Optional[datetime] = Field(None, alias="started-at")
    hora_fin: Optional[datetime] = Field(None, alias="finished-at")
    
    # Vehículo y Cliente
    placas: Optional[str] = Field(None, alias="license-plate")
    marca: Optional[str] = None
    modelo: Optional[str] = None
    color: Optional[str] = None
    nombre_cliente: Optional[str] = Field(None, alias="nombre-cliente")
    notas: Optional[str] = Field(None, alias="notes")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
