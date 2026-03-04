from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app import models, schemas


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user_in: schemas.UserCreate):
    hashed_password = get_password_hash(user_in.password)
    
    default_role = db.query(models.Role).filter(models.Role.name == "admin").first()
    
    if not default_role:
        raise ValueError("El rol predeterminado 'user' no existe en la base de datos")

    db_user = models.User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed_password,
        phone_number=user_in.phone_number,
        role_id=default_role.id
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def update_user(db: Session, user_id: int, user_in: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    update_data = user_in.model_dump(exclude_unset=True)
    # Nunca permitir cambio de password por aquí
    if "password" in update_data:
        raise ValueError("Use dedicated change-password endpoint")

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return {"ok": True}