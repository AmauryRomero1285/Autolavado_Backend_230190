'''
Docstring for models.modelUser
'''
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Date , ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class User(Base):
    ''' Docstring for User'''
    __tablename__ = "tbb_users"
    Id = Column(Integer, primary_key=True, index=True)
    rol_Id = Column(Integer, ForeignKey("tbc_roles.Id"))
    nombre = Column(String(60))
    papellido = Column(String(60))
    sapellido = Column(String(60))
    usuario = Column(String(60))
    contrasena = Column(String(60))
    telefono = Column(String(10))   
    estatus = Column(Boolean)
    fecha_registro = Column(DateTime)
    fecha_modificacion = Column(DateTime)