from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from app.schemas.products import ProductRead, ProductCreate, ProductUpdate
from app.crud import products as crud_product

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductRead])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_product.get_products(db, skip=skip, limit=limit)

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db=db, product=product)

@router.get("/{product_id}", response_model=ProductRead)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_product.get_product(db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_product

@router.patch("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud_product.update_product(db, product_id, product_update)
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    if not crud_product.delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return None
