from sqlalchemy.orm import Session
from app import models, schemas


def get_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Service).offset(skip).limit(limit).all()


def get_service(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id).first()


def create_service(db: Session, service_in: schemas.ServiceCreate):
    db_service = models.Service(
        name=service_in.name,
        description=service_in.description,
        price=service_in.price,
        duration_minutes=service_in.duration_minutes,
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def update_service(db: Session, service_id: int, service_in: schemas.ServiceUpdate):
    db_service = get_service(db, service_id)
    if not db_service:
        return None

    update_data = service_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_service, key, value)

    db.commit()
    db.refresh(db_service)
    return db_service


def delete_service(db: Session, service_id: int):
    db_service = get_service(db, service_id)
    if not db_service:
        return None
    db.delete(db_service)
    db.commit()
    return {"ok": True}