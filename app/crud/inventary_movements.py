#crud/inventary_movements.py

from sqlalchemy.orm import Session
from app.models.inventary_movements import InventaryMovement
from app.models.products import Product
from app.schemas.inventary_movements import InventoryCreate

def create_movement(db: Session, movement: InventoryCreate):
    db_movement = InventaryMovement(**movement.model_dump())
    db.add(db_movement)
    
    db_product = db.query(Product).filter(Product.id == movement.product_id).first()
    
    if db_product:
        if movement.type == "IN":
            db_product.stock += movement.quantity
        else:
            db_product.stock -= movement.quantity
            
    db.commit()
    db.refresh(db_movement)
    return db_movement

def get_movements_by_product(db: Session, product_id: int, skip: int = 0, limit: int = 100):
    return db.query(InventaryMovement)\
             .filter(InventaryMovement.product_id == product_id)\
             .order_by(InventaryMovement.created_at.desc())\
             .offset(skip).limit(limit).all()

def get_movement(db: Session, movement_id: int):
    return db.query(InventaryMovement).filter(InventaryMovement.id == movement_id).first()
