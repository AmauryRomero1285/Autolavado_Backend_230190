from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import config.db, crud.crud_usuario_vehiculo_servicio,  schemas.schema_usuario_vehiculo_servicio, models.model_usuario_vehiculo_servicio
from typing import List

usuario_vehiculo_servicio = APIRouter()
models.model_usuario_vehiculo_servicio.Base.metadata.create_all(bind=config.db.engine)    
def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()
@usuario_vehiculo_servicio.get("/usuario_vehiculo_servicio/", response_model=List[schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio], tags=["Usuario Vehiculo Servicios"])
async def read_usuario_vehiculo_servicios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_usuario_vehiculo_servicio= crud.crud_usuario_vehiculo_servicio.get_usuario_vehiculo_servicio(db=db, skip=skip, limit=limit)
    return db_usuario_vehiculo_servicio

@usuario_vehiculo_servicio.post("/usuario_vehiculo_servicio/", response_model=schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio, tags=["Usuario Vehiculo Servicios"])
async def create_usuario_vehiculo_servicio(usuario_vehiculo_servicio: schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicioCreate, db: Session = Depends(get_db)):
    db_usuario_vehiculo_servicio = crud.crud_usuario_vehiculo_servicio.create_usuario_vehiculo_servicio(db=db, usuario_vehiculo_servicio=usuario_vehiculo_servicio)
    return db_usuario_vehiculo_servicio

@usuario_vehiculo_servicio.delete("/usuario_vehiculo_servicio/{usuario_vehiculo_servicio_id}", tags=["Usuario Vehiculo Servicios"])
async def delete_usuario_vehiculo_servicio(usuario_vehiculo_servicio_id: int, db: Session = Depends(get_db)):
    db_usuario_vehiculo_servicio = crud.crud_usuario_vehiculo_servicio.delete_usuario_vehiculo_servicio(db=db, usuario_vehiculo_servicio_id=usuario_vehiculo_servicio_id)
    if db_usuario_vehiculo_servicio is None:
        raise HTTPException(status_code=404, detail="Usuario Vehiculo Servicio no encontrado")
    return {"detail": "Usuario Vehiculo Servicio eliminado exitosamente"}

@usuario_vehiculo_servicio.put("/usuario_vehiculo_servicio/{usuario_vehiculo_servicio_id}", response_model=schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio, tags=["Usuario Vehiculo Servicios"])
async def update_usuario_vehiculo_servicio(usuario_vehiculo_servicio_id: int, usuario_vehiculo_servicio: schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicioUpdate, db: Session = Depends(get_db)):
    db_usuario_vehiculo_servicio = crud.crud_usuario_vehiculo_servicio.update_usuario_vehiculo_servicio(db=db, usuario_vehiculo_servicio_id=usuario_vehiculo_servicio_id, usuario_vehiculo_servicio=usuario_vehiculo_servicio)
    if db_usuario_vehiculo_servicio is None:
        raise HTTPException(status_code=404, detail="Usuario Vehiculo Servicio no encontrado")
    return db_usuario_vehiculo_servicio
