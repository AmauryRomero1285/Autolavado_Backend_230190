# app/api/v1/roles.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app import crud, schemas
from app.api.v1.deps import DBSession, get_current_admin

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/", response_model=List[schemas.RoleRead])
def get_roles(
    db: DBSession,
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_admin),
):
    return crud.role.get_roles(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.RoleRead, status_code=201)
def create_role(
    role_in: schemas.RoleCreate,
    db: DBSession,
    current_user=Depends(get_current_admin),
):
    if crud.role.get_role_by_name(db, name=role_in.name):
        raise HTTPException(status_code=400, detail="El rol ya existe")
    return crud.role.create_role(db, role_in=role_in)


@router.patch("/{role_id}", response_model=schemas.RoleRead)
def update_role(
    role_id: int,
    role_in: schemas.RoleUpdate,
    db: DBSession,
    current_user=Depends(get_current_admin),
):
    role = crud.role.update_role(db, role_id=role_id, role_in=role_in)
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return role


@router.delete("/{role_id}")
def delete_role(
    role_id: int,
    db: DBSession,
    current_user=Depends(get_current_admin),
):
    result = crud.role.delete_role(db, role_id=role_id)
    if not result:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"detail": "Rol eliminado"}