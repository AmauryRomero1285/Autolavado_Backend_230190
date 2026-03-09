from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app import crud, schemas
from app.api.v1.deps import DBSession, get_current_active_user, get_current_staff, get_current_admin
from app.models.vehicle_service import VehicleService

router = APIRouter(prefix="/vehicle-services", tags=["vehicle-services"])

@router.post("/", response_model=schemas.VehicleServiceRead, status_code=status.HTTP_201_CREATED)
def create_order(db: DBSession, order_in: schemas.VehicleServiceCreate, current_user: schemas.UserRead = Depends(get_current_active_user)):
    vehicle = crud.vehicle.get_vehicle(db, vehicle_id=order_in.vehicle_id)
    if not vehicle: raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        
    service = crud.service.get_service(db, service_id=order_in.service_id)
    if not service: raise HTTPException(status_code=404, detail="Servicio no encontrado")

    if order_in.service_price is None:
        order_in.service_price = service.price

    return crud.vehicle_service.create_vehicle_service(db, obj_in=order_in)

@router.get("/", response_model=List[schemas.VehicleServiceRead])
def read_all_orders(db: DBSession, current_user: schemas.UserRead = Depends(get_current_staff)):
    return db.query(VehicleService).all()

@router.get("/{order_id}", response_model=schemas.VehicleServiceRead)
def read_order(order_id: int, db: DBSession, current_user: schemas.UserRead = Depends(get_current_active_user)):
    db_obj = crud.vehicle_service.get_vehicle_service(db, id=order_id)
    if not db_obj: raise HTTPException(status_code=404, detail="Orden no encontrada")
    return db_obj

@router.patch("/{order_id}", response_model=schemas.VehicleServiceRead)
def update_order(order_id: int, order_update: schemas.VehicleServiceUpdate, db: DBSession, current_user: schemas.UserRead = Depends(get_current_staff)):
    db_obj = crud.vehicle_service.update_status(db, id=order_id, status_update=order_update)
    if not db_obj: raise HTTPException(status_code=404, detail="Orden no encontrada")
    return db_obj

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: DBSession, current_user: schemas.UserRead = Depends(get_current_admin)):
    """Elimina una orden de servicio (Solo Admin)."""
    success = crud.vehicle_service.delete_vehicle_service(db, id=order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return None
