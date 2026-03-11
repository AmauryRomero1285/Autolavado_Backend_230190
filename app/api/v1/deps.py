"""
Dependencias reutilizables para los endpoints de la API v1.
"""
from typing import Annotated, Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models
from app.core import security                
from app.core.config import settings
from db import SessionLocal

# ───────────────────────────────────────────────
# ESQUEMA DE SEGURIDAD Y AUTENTICACIÓN
# ───────────────────────────────────────────────
# Usamos auto_error=False para que la misma instancia sirva para casos opcionales
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login", 
    scheme_name="JWT",
    description="Token JWT obtenido al hacer login (Bearer <token>)",
    auto_error=False
)

# ───────────────────────────────────────────────
#  Dependencia de Base de Datos
# ───────────────────────────────────────────────
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DBSession = Annotated[Session, Depends(get_db)]

# ───────────────────────────────────────────────
#  Lógica de Validación (Helper Interno)
# ───────────────────────────────────────────────
async def _get_user_from_token(db: Session, token: str) -> Optional[models.User]:
    """Valida el token y devuelve el usuario si todo es correcto."""
    try:
        # 1. Validar si el token existe en la DB y está activo (Logout Check)
        session_record = crud.auth.get_session_by_token(db, token=token)
        if not session_record or not session_record.is_active:
            return None

        # 2. Decodificar JWT
        secret_key = settings.SECRET_KEY 
        if hasattr(secret_key, "get_secret_value"):
            secret_key = secret_key.get_secret_value()

        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[security.ALGORITHM],
        )
        user_id_str: str | None = payload.get("sub")
        if not user_id_str:
            return None
            
        # 3. Obtener el usuario de la DB
        return crud.user.get_user_by_id(db, user_id=int(user_id_str))
    except (JWTError, ValueError, ValidationError, AttributeError):
        return None

# ───────────────────────────────────────────────
#  Dependencias de Usuario (Principales)
# ───────────────────────────────────────────────

async def get_current_user(
    db: DBSession,
    token: Annotated[Optional[str], Depends(oauth2_scheme)],
) -> models.User:
    """Requiere autenticación obligatoria."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionaron credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await _get_user_from_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o sesión expirada",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
) -> models.User:
    """Verifica que el usuario esté activo."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user

async def get_current_active_user_optional(
    db: DBSession,
    token: Annotated[Optional[str], Depends(oauth2_scheme)],
) -> Optional[models.User]:
    """Retorna el usuario si el token es válido, si no, retorna None sin error."""
    if not token:
        return None
    
    user = await _get_user_from_token(db, token)
    if user and user.is_active:
        return user
    return None

# ───────────────────────────────────────────────
#  Dependencias de Roles y Permisos
# ───────────────────────────────────────────────

def get_current_admin(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
) -> models.User:
    role_name = current_user.role.name.lower() if current_user.role else ""
    if role_name not in {"admin", "administrador"}:
        raise HTTPException(status_code=403, detail="Se requiere rol de administrador")
    return current_user

def get_current_staff(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
) -> models.User:
    if not current_user.role:
        raise HTTPException(status_code=403, detail="Rol no asignado")

    allowed_roles = {"admin", "administrador", "employee", "empleado", "cashier", "cajero"}
    if current_user.role.name.lower() not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: Se requiere rol de Staff"
        )
    return current_user

def get_current_client(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
) -> models.User:
    role_name = current_user.role.name.lower() if current_user.role else ""
    if role_name not in {"user", "cliente"}:
        raise HTTPException(status_code=403, detail="Se requiere rol de cliente")
    return current_user

def check_can_register_admin(db: DBSession):
    """
    Regla: Solo permite el registro si NO existen administradores.
    Si ya hay uno, exige que el que está registrando sea ADMIN.
    """
    admin_exists = db.query(models.User).join(models.Role).filter(
        models.Role.name.ilike("admin")
    ).first()
    
    if not admin_exists:
        return True

    return False