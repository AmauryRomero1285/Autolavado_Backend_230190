from sqlalchemy.orm import Session
from app.models.vehicle_service import VehicleService
from app.schemas.vehicle_service import VehicleServiceCreate, VehicleServiceUpdate

def get_vehicle_service(db: Session, id: int):
    """Obtiene una orden de servicio específica por su ID"""
    return db.query(VehicleService).filter(VehicleService.id == id).first()

def get_by_vehicle(db: Session, vehicle_id: int):
    """Obtiene todas las órdenes de servicio de un vehículo"""
    return db.query(VehicleService).filter(VehicleService.vehicle_id == vehicle_id).all()

def create_vehicle_service(db: Session, *, obj_in: VehicleServiceCreate):
    """Crea una nueva orden con limpieza de IDs y cálculo opcional de total."""
    data = obj_in.model_dump()
    
    # Limpieza de ceros para MySQL Foreign Keys
    if data.get("employee_casher_id") == 0: data["employee_casher_id"] = None
    if data.get("employee_washer_id") == 0: data["employee_washer_id"] = None
    
    # Cálculo automático de total_price si se proveen precios pero no el total
    if data.get("service_price") is not None and data.get("total_price") is None:
        discount = data.get("discount") or 0
        data["total_price"] = data["service_price"] - discount

    db_obj = VehicleService(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_status(db: Session, id: int, status_update: VehicleServiceUpdate):
    """Actualiza parcialmente una orden de servicio."""
    db_obj = get_vehicle_service(db, id=id)
    if db_obj:
        update_data = status_update.model_dump(exclude_unset=True)
        
        if update_data.get("employee_casher_id") == 0: update_data["employee_casher_id"] = None
        if update_data.get("employee_washer_id") == 0: update_data["employee_washer_id"] = None
            
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        db.commit()
        db.refresh(db_obj)
    return db_obj

def delete_vehicle_service(db: Session, id: int):
    """Elimina físicamente un registro de la tabla intermedia"""
    db_obj = get_vehicle_service(db, id=id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
        return True
    return False
