'''
Docstring for models.serviciovehiculo
'''
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Date , ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base
class ServicioVehiculo(Base):
    ''' Docstring for ServicioVehiculo'''
    __tablename__ = "tbd_serviciovehiculo"
    Id = Column(Integer, primary_key=True, index=True)
    cajero_Id = Column(Integer, ForeignKey("tbc_users.Id"))
    lavador_Id = Column(Integer, ForeignKey("tbc_users.Id"))
    servicio_Id = Column(Integer, ForeignKey("tbc_servicio.Id"))
    vehiculo_Id = Column(Integer, ForeignKey("tbc_vehiculo.Id"))
    fecha = Column(DateTime)
    estatus = Column(Boolean)
    fecha_registro = Column(DateTime)
    fecha_modificacion = Column(DateTime)