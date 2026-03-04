# app/api/v1/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app import crud, schemas
from app.api.v1.deps import get_current_active_user,get_current_admin, DBSession


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[schemas.UserRead])
def get_users(
    db: DBSession,
    skip: int = 0,
    limit: int = 100,
    # Cambiamos a get_current_admin para restringir el acceso
    current_user=Depends(get_current_admin), 
):
    """
    Solo los administradores pueden listar todos los usuarios.
    """
    return crud.user.get_users(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.UserRead, status_code=201)
def create_user(
    user_in: schemas.UserCreate,
    db: DBSession,
    current_user=Depends(get_current_active_user),
):
    if crud.user.get_user_by_email(db, email=user_in.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return crud.user.create_user(db, user_in=user_in)


@router.get("/me", response_model=schemas.UserRead)
def read_current_user(current_user=Depends(get_current_active_user)):  # del deps
    return current_user


@router.patch("/{user_id}", response_model=schemas.UserRead)
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: DBSession,
    current_user=Depends(get_current_active_user),
):
    user = crud.user.update_user(db, user_id=user_id, user_in=user_in)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user