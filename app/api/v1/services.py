# app/api/v1/services.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app import crud, schemas
from app.api.v1.deps import DBSession, get_current_admin

router = APIRouter(prefix="/services", tags=["services"])


@router.get("/", response_model=List[schemas.ServiceRead])
def get_services(
    db: DBSession,
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_employee_or_admin),  # empleados también pueden ver
):
    return crud.service.get_services(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.ServiceRead, status_code=201)
def create_service(
    service_in: schemas.ServiceCreate,
    db: DBSession,
    current_user=Depends(get_current_admin),
):
    return crud.service.create_service(db, service_in=service_in)


@router.patch("/{service_id}", response_model=schemas.ServiceRead)
def update_service(
    service_id: int,
    service_in: schemas.ServiceUpdate,
    db: DBSession,
    current_user=Depends(get_current_admin),
):
    service = crud.service.update_service(db, service_id=service_id, service_in=service_in)
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return service


@router.delete("/{service_id}")
def delete_service(
    service_id: int,
    db: DBSession,
    current_user=Depends(get_current_admin),
):
    result = crud.service.delete_service(db, service_id=service_id)
    if not result:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return {"detail": "Servicio eliminado"}