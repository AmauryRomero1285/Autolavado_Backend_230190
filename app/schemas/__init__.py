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
    Token,             
)

from .role import RoleBase, RoleCreate, RoleUpdate, RoleRead, RoleMinimal
from .client import ClientBase, ClientCreate, ClientUpdate, ClientRead
from .vehicle import VehicleBase, VehicleCreate, VehicleUpdate, VehicleRead, VehicleMinimal
from .services import ServiceBase,ServiceCreate,ServiceUpdate,ServiceRead,ServiceMinimal
from .vehicle_service import VehicleServiceBase, VehicleServiceCreate, VehicleServiceUpdate, VehicleServiceRead
from .products import ProductBase, ProductCreate, ProductUpdate, ProductRead, ProductMinimal 
from .inventary_movements import InventoryBase, InventoryCreate, InventoryRead, InventoryUpdate
