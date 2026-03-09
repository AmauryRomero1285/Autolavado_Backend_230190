# app/api/v1/vehicles.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app import crud, schemas
from app.api.v1.deps import DBSession, get_current_staff

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/", response_model=List[schemas.VehicleRead])
def get_vehicles(
    db: DBSession,
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_staff),
):
    return crud.vehicle.get_vehicles(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.VehicleRead, status_code=201)
def create_vehicle(
    vehicle_in: schemas.VehicleCreate,
    db: DBSession,
    current_user=Depends(get_current_staff),
):
    # Validación extra: que el cliente exista
    client = crud.client.get_client(db, client_id=vehicle_in.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    return crud.vehicle.create_vehicle(db, vehicle_in=vehicle_in)


@router.get("/{vehicle_id}", response_model=schemas.VehicleRead)
def get_vehicle(
    vehicle_id: int,
    db: DBSession,
    current_user=Depends(get_current_staff),
):
    vehicle = crud.vehicle.get_vehicle(db, vehicle_id=vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehicle


@router.patch("/{vehicle_id}", response_model=schemas.VehicleRead)
def update_vehicle(
    vehicle_id: int,
    vehicle_in: schemas.VehicleUpdate,
    db: DBSession,
    current_user=Depends(get_current_staff),
):
    vehicle = crud.vehicle.update_vehicle(db, vehicle_id=vehicle_id, vehicle_in=vehicle_in)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehicle