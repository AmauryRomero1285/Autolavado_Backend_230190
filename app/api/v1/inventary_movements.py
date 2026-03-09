# app/api/v1/inventory_movements.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from app.schemas.inventary_movements import InventoryRead, InventoryCreate
from app.crud import inventary_movements as crud_inventory
from app.crud import products as crud_product

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.post("/", response_model=InventoryRead, status_code=status.HTTP_201_CREATED)
def create_inventory_movement(movement: InventoryCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el producto existe
    db_product = crud_product.get_product(db, product_id=movement.product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="El producto especificado no existe"
        )
    
    # 2. Validación: No permitir salidas si no hay stock suficiente
    if movement.type == "OUT" and db_product.stock < movement.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock insuficiente. Disponible: {db_product.stock}"
        )

    return crud_inventory.create_movement(db=db, movement=movement)

@router.get("/product/{product_id}", response_model=List[InventoryRead])
def read_movements_by_product(
    product_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    movements = crud_inventory.get_movements_by_product(db, product_id=product_id, skip=skip, limit=limit)
    return movements

@router.get("/{movement_id}", response_model=InventoryRead)
def read_movement(movement_id: int, db: Session = Depends(get_db)):
    db_movement = crud_inventory.get_movement(db, movement_id=movement_id)
    if not db_movement:
        raise HTTPException(status_code=404, detail="Movimiento de inventario no encontrado")
    return db_movement
