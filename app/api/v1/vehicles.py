from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import config.db, crud.crud_vehiculos,  schemas.schema_vehiculos, models.modelVehiculos
from typing import List
vehiculo = APIRouter()
models.modelVehiculos.Base.metadata.create_all(bind=config.db.engine)
def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()