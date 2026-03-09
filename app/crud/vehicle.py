from sqlalchemy.orm import Session
from app import models, schemas


def get_vehicles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle).offset(skip).limit(limit).all()


def get_vehicle(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()


def create_vehicle(db: Session, vehicle_in: schemas.VehicleCreate):
    db_vehicle = models.Vehicle(
        license_plate=vehicle_in.license_plate,
        brand=vehicle_in.brand,
        model=vehicle_in.model,
        color=vehicle_in.color,
        vehicle_type=vehicle_in.vehicle_type,
        year=vehicle_in.year,
        client_id=vehicle_in.client_id,  # asumiendo que viene en el esquema
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


def update_vehicle(db: Session, vehicle_id: int, vehicle_in: schemas.VehicleUpdate):
    db_vehicle = get_vehicle(db, vehicle_id)
    if not db_vehicle:
        return None

    update_data = vehicle_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_vehicle, key, value)

    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


def delete_vehicle(db: Session, vehicle_id: int):
    db_vehicle = get_vehicle(db, vehicle_id)
    if not db_vehicle:
        return None
    db.delete(db_vehicle)
    db.commit()
    return {"ok": True}