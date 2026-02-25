import models.vehicle_services_model
import schemas.vehicle_services_schema
from sqlalchemy.orm import Session

def get_vehicle_service(db: Session, skip: int = 0, limit: int = 10):
    '''Función para obtener un usuario_vehiculo_servicio por su ID'''
    return db.query(models.vehicle_services_model.VehicleService).offset(skip).limit(limit).all()

def create_vehicle_service(db: Session, vehicle_service: schemas.vehicle_services_schema.VehicleServiceCreate):
    '''Función para crear un nuevo usuario_vehiculo_servicio'''
    db_vehicle_service = models.vehicle_services_model.VehicleService(
        vehicle_id=vehicle_service.vehicle_id,
        service_id=vehicle_service.service_id,
        created_at=vehicle_service.created_at
    )
    db.add(db_vehicle_service)
    db.commit()
    db.refresh(db_vehicle_service)
    return db_vehicle_service

def update_vehicle_service(db: Session, id: int, vehicle_service: schemas.vehicle_services_schema.VehicleServiceUpdate):
    '''Función para actualizar un usuario_vehiculo_servicio existente'''
    db_vehicle_service= db.query(models.vehicle_services_model.VehicleService).filter(models.vehicle_services_model.VehicleService.id==id).first()
    if db_vehicle_service is None:
        return None
    db_vehicle_service.vehicle_id = vehicle_service.vehicle_id
    db_vehicle_service.servicio_Id = vehicle_service.service_id
    db_vehicle_service.fecha_registro = vehicle_service.created_at
    db.commit()
    db.refresh(db_vehicle_service)
    return db_vehicle_service

def delete_usuario_vehiculo_servicio(db: Session, id: int):
    '''Función para eliminar un usuario_vehiculo_servicio por su ID'''
    db_vehicle_services = db.query(models.vehicle_services_model.VehicleService).filter(models.vehicle_services_model.VehicleService.id == id).first()
    if db_vehicle_services is None:
        return None
    db.delete(db_vehicle_services)
    db.commit()
    return db_vehicle_services

