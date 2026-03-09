# schemas/role.py
"""
Esquemas Pydantic para la entidad Role en la API de autolavado.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class RoleBase(BaseModel):
    """Campos comunes seguros para lectura y base de otros esquemas."""
    name: str = Field(
        ...,
        min_length=3,
        max_length=60,
        description="Nombre único del rol (ej: admin, employee, customer)"
    )
    is_active: bool = Field(
        default=True,
        description="Indica si el rol está activo y puede asignarse"
    )


class RoleCreate(BaseModel):
    """Esquema para creación de roles (POST /roles) – solo admin."""
    name: str = Field(
        ...,
        min_length=3,
        max_length=60,
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="Nombre del rol (solo letras, números, guiones y underscore)"
    )


class RoleUpdate(BaseModel):
    """Esquema para actualización parcial de roles (PATCH /roles/{id}) – solo admin."""
    name: Optional[str] = Field(
        None,
        min_length=3,
        max_length=60,
        pattern=r"^[a-zA-Z0-9_-]+$",
    )
    is_active: Optional[bool] = None


class RoleRead(RoleBase):
    """Esquema de respuesta completa y segura para roles."""
    id: int = Field(..., description="Identificador único del rol")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )


# Opcional: esquema mínimo para usar en otras respuestas (ej: UserRead)
class RoleMinimal(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)