import models.role_model
import schemas.role_schema

from sqlalchemy.orm import Session

def get_rol(db:Session, skip: int =0, limit:int=10):
    return db.query(models.role_model.Role).offset(skip).limit(limit).all()
    
def get_rol_by_name(db:Session,name:str):
    return db.query(models.role_model.Role).filter(models.role_model.Role.name == name).first()

def create_rol(db:Session, role:schemas.role_schema.RolCreate):
    db_role=models.role_model.Role(
        name=role.name,
        is_active=role.is_active,
        created_at=role.created_at,
        updated_at=role.updated_at
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db:Session, id:int,rol:schemas.role_schema.RoleUpdate):
    db_role=db.query()
