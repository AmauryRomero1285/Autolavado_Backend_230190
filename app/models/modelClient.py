'''
Docstring for models.cliente
'''
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Date , ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Cliente(Base):
    ''' Docstring for Cliente'''
    __tablename__ = "tbc_cliente"
    Id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(60))
    papellido = Column(String(60))
    sapellido = Column(String(60))
    direccion = Column(String(60))
    telefono = Column(String(10))   
    estatus = Column(Boolean)
    fecha_registro = Column(DateTime)
    fecha_modificacion = Column(DateTime)