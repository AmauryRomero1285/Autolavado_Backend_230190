# app/api/v1/deps.py
"""
Dependencias reutilizables para los endpoints de la API v1.
"""
from typing import Annotated, Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security                
from app.core.config import settings
from db import SessionLocal

# ───────────────────────────────────────────────
#  OAuth2 scheme corregido (Ruta relativa)
# ───────────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login", # Relativo para evitar conflictos de prefijo /api/v1
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
#Seleccion de rol para registro 
# ───────────────────────────────────────────────

optional_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login", 
    auto_error=False 
)

async def get_current_active_user_optional(
    db: DBSession,
    token: Annotated[Optional[str], Depends(optional_oauth2_scheme)] = None,
) -> Optional[models.User]:
    if not token:
        
        return None
    try:
        user = await get_current_user(token, db)
        return await get_current_active_user(user)
    except HTTPException:
        return None


# ───────────────────────────────────────────────
#  Usuario autenticado (Con verificación de sesión activa)
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

    # 1. Validar si el token está activo en la DB (Logout Check)
    session_record = crud.auth.get_session_by_token(db, token=token)
    if not session_record or not session_record.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión cerrada o token inválido",
        )

    # 2. Decodificar el JWT
    try:
        # CORRECCIÓN: Se eliminó .get_secret_value() porque SECRET_KEY es str
        secret_key = settings.SECRET_KEY 
        if hasattr(secret_key, "get_secret_value"):
            secret_key = secret_key.get_secret_value()

        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[security.ALGORITHM],
        )
        user_id_str: str | None = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (JWTError, ValueError, ValidationError):
        raise credentials_exception

    # 3. Obtener el usuario de la DB
    user = crud.user.get_user_by_id(db, user_id=user_id)

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
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user


# ───────────────────────────────────────────────
#  Solo administradores
# ───────────────────────────────────────────────
def get_current_admin(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
) -> models.User:
    # Verificación flexible de rol
    role_name = current_user.role.name.lower() if current_user.role else ""
    if role_name not in {"admin", "administrador"}:
        raise HTTPException(status_code=403, detail="Se requiere rol de administrador")
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

# ───────────────────────────────────────────────
#  Solo Clientes (User)
# ───────────────────────────────────────────────
def get_current_client(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
) -> models.User:
    """Verifica que el usuario tenga el rol de cliente/usuario estándar"""
    if not current_user.role or current_user.role.name.lower() not in {"user", "cliente"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de cliente/usuario",
        )
    return current_user