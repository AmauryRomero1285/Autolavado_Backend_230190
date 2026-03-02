# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.v1.deps import DBSession
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register(
    user_in: schemas.UserCreate,
    db: DBSession,
):
    """
    Registrar un nuevo usuario (Cliente).
    """
    # 1. Verificar si el email ya existe
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Este correo electrónico ya está registrado.",
        )
    
    # 2. Verificar si el teléfono ya existe (si aplica)
    # user_phone = crud.user.get_by_phone(db, phone=user_in.phone_number)
    
    # 3. Crear el usuario usando tu CRUD
    new_user = crud.user.create(db, obj_in=user_in)
    return new_user


@router.post("/login", response_model=schemas.Token)
def login(
    user_login: schemas.UserLogin,
    db: DBSession,
):
    """Login con email o teléfono (identifier)"""
    # Buscar por email o por teléfono
    user = crud.user.get_user_by_email(db, email=user_login.identifier)
    if not user:
        # Intentar por teléfono (si el identifier es numérico)
        if user_login.identifier.replace("+", "").isdigit():
            user = db.query(crud.models.User).filter(
                crud.models.User.phone_number == user_login.identifier
            ).first()

    if not user or not verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return schemas.Token(access_token=access_token, token_type="bearer")