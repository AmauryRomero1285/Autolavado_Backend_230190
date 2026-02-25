from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import config.db, services.service_services,  schemas.services_schema, models.services_model
from typing import List


servicio = APIRouter()

models.modelServicio.Base.metadata.create_all(bind=config.db.engine)   
def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()
@servicio.get("/servicio/", response_model=List[schemas.schema_servicio.Servicio], tags=["Servicio"])        
async def read_servicio(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    '''Función para obtener un servicio por su ID'''
    db_servicio = crud.crud_servicio.get_servicio(db, skip=skip, limit=limit)
    return db_servicio  

@servicio.post("/servicio/", response_model=schemas.schema_servicio.Servicio, tags=["Servicio"])
async def create_servicio(servicio: schemas.schema_servicio.ServicioCreate, db: Session = Depends(get_db)):
    '''Función para crear un nuevo servicio'''
    db_servicio = crud.crud_servicio.create_servicio(db=db, servicio=servicio)
    return db_servicio

@servicio.delete("/servicio/{servicio_id}", tags=["Servicio"])
async def delete_servicio(servicio_id: int, db: Session = Depends(get_db)):
    '''Función para eliminar un servicio por su ID'''
    db_servicio = crud.crud_servicio.delete_servicio(db=db, servicio_id=servicio_id)
    if db_servicio is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return {"detail": "Servicio eliminado exitosamente"}

@servicio.put("/servicio/{servicio_id}", response_model=schemas.schema_servicio.Servicio, tags=["Servicio"])
async def update_servicio(servicio_id: int, servicio: schemas.schema_servicio.ServicioUpdate, db: Session = Depends(get_db)):
    '''Función para actualizar un servicio por su ID'''
    db_servicio = crud.crud_servicio.update_servicio(db=db, servicio_id=servicio_id, servicio=servicio)
    if db_servicio is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return db_servicio

