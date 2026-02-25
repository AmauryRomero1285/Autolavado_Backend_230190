from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import config.db, models.role_model, schemas.role_schema, services.role_services

rol_router = APIRouter()

models.role_model.Base.metadata.create_all(bind=config.db.engine)    

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@rol_router.get("/role/", response_model=list[schemas.role_schema.Role], tags=["Role"])        
async def read_role(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    '''Función para obtener un rol por su ID'''
    db_rol = services.role_services.get_rol(db, skip=skip, limit=limit)
    return db_rol

@rol_router.post("/role/create/", response_model=schemas.role_schema.RolCreate, tags=["Role"])
async def create_role(rol: schemas.role_schema.RolCreate, db: Session = Depends(get_db)):
    '''Función para crear un nuevo rol'''
    db_rol = services.role_services.create_rol(db=db, rol=rol)
    return db_rol

@rol_router.delete("/role/{rol_id}", tags=["Role"])
async def delete_role(id: int, db: Session = Depends(get_db)):
    '''Función para eliminar un rol por su ID'''
    db_rol = services.role_services.delete_role(db=db, rol_id=id)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"detail": "Rol eliminado exitosamente"}

@rol_router.put("/role/{rol_id}", response_model=schemas.role_schema.Role, tags=["Role"])
async def update_role(id: int, rol: schemas.role_schema.RoleUpdate, db: Session = Depends(get_db)):
    '''Función para actualizar un rol por su ID'''
    db_rol = services.role_services.update_role(db=db, rol_id=id, rol=rol)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return db_rol