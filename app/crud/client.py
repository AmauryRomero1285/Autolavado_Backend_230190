# app/crud/client.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app import models, schemas
from app.core.exceptions import DuplicatePhoneError  # opcional: excepción personalizada


def get_clients(db: Session, skip: int = 0, limit: int = 100) -> List[models.Client]:
    """Obtiene una lista paginada de clientes"""
    return db.query(models.Client).offset(skip).limit(limit).all()


def get_client(db: Session, client_id: int) -> Optional[models.Client]:
    """Obtiene un cliente por su ID"""
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def get_client_by_phone(db: Session, phone_number: str) -> Optional[models.Client]:
    """Obtiene un cliente por número de teléfono (normalizado o exacto)"""
    return db.query(models.Client).filter(models.Client.phone_number == phone_number).first()


def get_client_by_user_id(db: Session, user_id: int) -> Optional[models.Client]:
    """Obtiene el cliente asociado a un usuario registrado (si existe)"""
    return db.query(models.Client).filter(models.Client.user_id == user_id).first()


def create_client(db: Session, client_in: schemas.ClientCreate) -> models.Client:
    """
    Crea un nuevo cliente.
    Valida unicidad del teléfono antes de intentar guardar.
    """
    # Verificar si ya existe un cliente con ese teléfono
    if get_client_by_phone(db, client_in.phone_number):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un cliente registrado con ese número de teléfono"
        )

    db_client = models.Client(**client_in.model_dump(exclude_unset=True))

    try:
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflicto de integridad (posible duplicado de teléfono)"
        )


def update_client(
    db: Session,
    client_id: int,
    client_in: schemas.ClientUpdate
) -> Optional[models.Client]:
    """Actualización parcial de un cliente"""
    db_client = get_client(db, client_id)
    if not db_client:
        return None

    update_data = client_in.model_dump(exclude_unset=True)

    # Validar unicidad de teléfono si se está actualizando
    if "phone_number" in update_data:
        existing = get_client_by_phone(db, update_data["phone_number"])
        if existing and existing.id != client_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El número de teléfono ya está en uso por otro cliente"
            )

    for key, value in update_data.items():
        setattr(db_client, key, value)

    db.commit()
    db.refresh(db_client)
    return db_client


def soft_delete_client(db: Session, client_id: int) -> Optional[dict]:
    """
    Desactiva lógicamente un cliente (soft delete)
    Preserva historial de vehículos y citas
    """
    db_client = get_client(db, client_id)
    if not db_client:
        return None

    db_client.is_active = False
    db.commit()
    db.refresh(db_client)
    
    return {"ok": True, "message": "Cliente desactivado correctamente"}


def hard_delete_client(db: Session, client_id: int) -> Optional[dict]:
    """
    Eliminación física (hard delete) - usar con precaución
    Solo recomendado para limpieza de datos de prueba o casos muy específicos
    """
    db_client = get_client(db, client_id)
    if not db_client:
        return None
    
    db.delete(db_client)
    db.commit()
    return {"ok": True, "message": "Cliente eliminado permanentemente"}