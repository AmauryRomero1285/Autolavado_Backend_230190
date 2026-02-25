from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import config.db, crud.crud_user,  schemas.schema_user, models.modelUser
from typing import List

user = APIRouter()
models.modelUser.Base.metadata.create_all(bind=config.db.engine)    
def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()
@user.get("/user/", response_model=List[schemas.schema_user.User], tags=["User"])        
async def read_user(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    '''Función para obtener un usuario por su ID'''
    db_user = crud.crud_user.get_user(db, skip=skip, limit=limit)
    return db_user

@user.post("/user/", response_model=schemas.schema_user.User, tags=["User"])
async def create_user(user: schemas.schema_user.UserCreate, db: Session = Depends(get_db)):
    '''Función para crear un nuevo usuario'''
    db_user = crud.crud_user.create_user(db=db, user=user)
    return db_user

@user.delete("/user/{user_id}", tags=["User"])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    '''Función para eliminar un usuario por su ID'''
    db_user = crud.crud_user.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"detail": "Usuario eliminado exitosamente"}

@user.put("/user/{user_id}", response_model=schemas.schema_user.User, tags=["User"])
async def update_user(user_id: int, user: schemas.schema_user.UserUpdate, db: Session = Depends(get_db)):
    '''Función para actualizar un usuario por su ID'''
    db_user = crud.crud_user.update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user
    

