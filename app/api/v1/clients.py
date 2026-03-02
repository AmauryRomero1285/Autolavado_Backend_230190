# app/api/v1/clients.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app import crud, schemas
from app.api.v1.deps import DBSession, get_current_staff,DBSession

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("/", response_model=List[schemas.ClientRead])
def get_clients(
    db: DBSession,
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_staff),
):
    return crud.client.get_clients(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.ClientRead, status_code=201)
def create_client(
    client_in: schemas.ClientCreate,
    db: DBSession,
    current_user=Depends(get_current_staff),
):
    if crud.client.get_client_by_phone(db, phone=client_in.phone_number):
        raise HTTPException(status_code=400, detail="Ya existe un cliente con ese teléfono")
    return crud.client.create_client(db, client_in=client_in)


@router.get("/{client_id}", response_model=schemas.ClientRead)
def get_client(
    client_id: int,
    db: DBSession,
    current_user=Depends(get_current_staff),
):
    client = crud.client.get_client(db, client_id=client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client


@router.patch("/{client_id}", response_model=schemas.ClientRead)
def update_client(
    client_id: int,
    client_in: schemas.ClientUpdate,
    db: DBSession,
    current_user=Depends(get_current_staff),
):
    client = crud.client.update_client(db, client_id=client_id, client_in=client_in)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client