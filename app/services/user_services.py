import models.user_model
import schemas.user_schema
from sqlalchemy.orm import Session

def get_user(db: Session, skip: int = 0, limit: int = 10):
    '''Función para obtener un usuario por su ID'''
    return db.query(models.user_model.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.user_schema.UserCreate):
    '''Función para crear un nuevo usuario'''
    db_user = models.user_model.User(
        name=user.first_name,
        email=user.email,
        password=user.password,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, id: int, user: schemas.user_schema.UserUpdate):
    '''Función para actualizar un usuario existente'''
    db_user = db.query(models.user_model.User).filter(models.user_model.User.id == id).first()
    if db_user is None:
        return None
    db_user.name = user.first_name
    db_user.email = user.email
    db_user.password = user.password
    db_user.is_active = user.is_active
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, id: int):
    '''Función para eliminar un usuario por su ID'''
    db_user = db.query(models.user_model.User).filter(models.user_model.User.id == id).first()
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

