# app/schemas/__init__.py
# ───────────────────────────────────────────────
# Exporta todos los esquemas públicos para que se puedan importar como:
# from app.schemas import UserCreate, Token, ClientRead, ...
# ───────────────────────────────────────────────

from .user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserRead,
    UserLogin,
    Token,               # ← agrega esto
)

from .role import RoleBase, RoleCreate, RoleUpdate, RoleRead, RoleMinimal
from .client import ClientBase, ClientCreate, ClientUpdate, ClientRead
from .vehicle import VehicleBase, VehicleCreate, VehicleUpdate, VehicleRead, VehicleMinimal