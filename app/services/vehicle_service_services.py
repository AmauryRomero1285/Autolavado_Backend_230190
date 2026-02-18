import models.vehicle_services_model
import schemas.vehicle_services_schema
from sqlalchemy.orm import Session

def get_vehicle_service(db: Session, skip: int = 0, limit: int = 10):
    '''Función para obtener un usuario_vehiculo_servicio por su ID'''
    return db.query(models.vehicle_services_model.VehicleService).offset(skip).limit(limit).all()

def create_vehicle_service(db: Session, vehicule_service: schemas.vehicle_services_schema.VehicleServiceCreate):
    '''Función para crear un nuevo usuario_vehiculo_servicio'''
    db_usuario_vehiculo_servicio = models.vehicle_services_model.VehicleService(
        user_id=,
        vehicle_id=usuario_vehiculo_servicio.vehiculo_Id,
        service_id=usuario_vehiculo_servicio.servicio_Id,
        created_at=usuario_vehiculo_servicio.fecha_registro
    )
    db.add(db_usuario_vehiculo_servicio)
    db.commit()
    db.refresh(db_usuario_vehiculo_servicio)
    return db_usuario_vehiculo_servicio

def update_usuario_vehiculo_servicio(db: Session, usuario_vehiculo_servicio_id: int, usuario_vehiculo_servicio: schemas.schema_usuario_vehiculo_servicio.Usuario_Vehiculo_ServicioUpdate):
    '''Función para actualizar un usuario_vehiculo_servicio existente'''
    db_usuario_vehiculo_servicio = db.query(models.model_usuario_vehiculo_servicio.Usuario_Vehiculo_Servicio).filter(models.model_usuario_vehiculo_servicio.Usuario_Vehiculo_Servicio.Id == usuario_vehiculo_servicio_id).first()
    if db_usuario_vehiculo_servicio is None:
        return None
    db_usuario_vehiculo_servicio.usuario_Id = usuario_vehiculo_servicio.usuario_Id
    db_usuario_vehiculo_servicio.vehiculo_Id = usuario_vehiculo_servicio.vehiculo_Id
    db_usuario_vehiculo_servicio.servicio_Id = usuario_vehiculo_servicio.servicio_Id
    db_usuario_vehiculo_servicio.fecha_registro = usuario_vehiculo_servicio.fecha_registro
    db.commit()
    db.refresh(db_usuario_vehiculo_servicio)
    return db_usuario_vehiculo_servicio

def delete_usuario_vehiculo_servicio(db: Session, usuario_vehiculo_servicio_id: int):
    '''Función para eliminar un usuario_vehiculo_servicio por su ID'''
    db_usuario_vehiculo_servicio = db.query(models.model_usuario_vehiculo_servicio.Usuario_Vehiculo_Servicio).filter(models.model_usuario_vehiculo_servicio.Usuario_Vehiculo_Servicio.Id == usuario_vehiculo_servicio_id).first()
    if db_usuario_vehiculo_servicio is None:
        return None
    db.delete(db_usuario_vehiculo_servicio)
    db.commit()
    return db_usuario_vehiculo_servicio

