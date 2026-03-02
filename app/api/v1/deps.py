# app/api/v1/deps.py
"""
Dependencias reutilizables para los endpoints de la API v1.
Centraliza la inyección de DB, usuario autenticado y chequeos de autorización.
"""
from typing import Annotated, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security                # asumiendo que aquí está ALGORITHM, SECRET_KEY, etc.
from app.core.config import settings
from db import SessionLocal


# ───────────────────────────────────────────────
#  OAuth2 scheme para extraer el token del header
# ───────────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    scheme_name="JWT",
    description="Token JWT obtenido al hacer login (Bearer <token>)"
)


# ───────────────────────────────────────────────
#  Dependencia base de sesión de base de datos
# ───────────────────────────────────────────────
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBSession = Annotated[Session, Depends(get_db)]


# ───────────────────────────────────────────────
#  Usuario autenticado (cualquier token válido)
# ───────────────────────────────────────────────
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DBSession,
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[security.ALGORITHM],
        )
        user_id_str: str | None = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (JWTError, ValueError, ValidationError):
        raise credentials_exception

    user = crud.user.get(db, id=user_id)
    if user is None:
        raise credentials_exception

    return user


# ───────────────────────────────────────────────
#  Usuario autenticado + activo
# ───────────────────────────────────────────────
async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user


# ───────────────────────────────────────────────
#  Solo administradores
# ───────────────────────────────────────────────
def get_current_admin(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
) -> models.User:
    if not current_user.role or current_user.role.name.lower() not in {"admin", "administrador"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador"
        )
    return current_user


# ───────────────────────────────────────────────
#  Empleados, cajeros o administradores
#   (operaciones operativas del lavado)
# ───────────────────────────────────────────────
def get_current_staff(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
) -> models.User:
    if not current_user.role:
        raise HTTPException(status_code=403, detail="Rol no asignado")

    allowed_roles = {"admin", "administrador", "employee", "empleado", "cashier", "cajero"}
    if current_user.role.name.lower() not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de empleado, cajero o administrador"
        )
    return current_user


# ───────────────────────────────────────────────
#  Solo el propio usuario (o admin)
#   Útil para endpoints /me o edición de perfil propio
# ───────────────────────────────────────────────
def get_current_user_or_admin(
    user_id: int,                       # se pasa desde path o query
    current_user: Annotated[models.User, Depends(get_current_active_user)]
) -> models.User:
    if current_user.id == user_id or \
       (current_user.role and current_user.role.name.lower() in {"admin", "administrador"}):
        return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permiso para acceder o modificar este recurso"
    )