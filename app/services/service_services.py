import models.services_model
import schemas.services_schema

from sqlalchemy.orm import Session

def get_service(db:Session, skip: int =0, limit:int=10):
    return db.query(models.services_model.Service).offset(skip).limit(limit).all()

def create_service(db:Session, service:schemas.services_schema.ServiceCreate):
    db_service=models.services_model.Service(
        name=service.name,
        description=service.description,
        price=service.price,
        is_active=service.is_active,
        created_at=service.created_at,
        updated_at=service.updated_at
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def update_service(db:Session, id:int,service:schemas.services_schema.ServiceUpdate):
    db_service=db.query(models.services_model.Service).filter(models.services_model.Service.id==id).first()
    if db_service is None : 
        return None
    db_service.name_service=service.name
    db_service.description=service.description
    db_service.price=service.price
    db_service.is_active=service.is_active
    db.commit()
    db.refresh(db_service)
    return db_service

def delete_service(db:Session, id:int):
    db_service=db.query(models.services_model.Service).filter(models.services_model.Service.id==id).first()
    if db_service is None:
        return None
    db.delete(db_service)
    db.commit()
    return db_service
