from fastapi import APIRouter, Depends

from .auth import router as auth_router
from .roles import router as roles_router
from .users import router as users_router
from .clients import router as clients_router
from .vehicles import router as vehicles_router
from .services import router as services_router
from .vehicle_service import router as vehicle_services
from .products import router as products_router
from .cashier import router as cashier_router 
from .inventary_movements import router as inventary_router

# Importamos las dependencias de autorización
from app.api.v1.deps import get_current_active_user, get_current_admin, get_current_client

api_router = APIRouter()

# --- RUTAS DE AUTENTICACIÓN (Públicas) ---
api_router.include_router(auth_router)

# --- RUTAS ACCESIBLES POR TODOS (USER/CLIENT, EMPLOYEE, ADMIN) ---
# Se incluyen aquí para permitir (GET)products, (POST)vehicles y /users/me
api_router.include_router(
    products_router,
    dependencies=[Depends(get_current_active_user)]
)
api_router.include_router(
    vehicles_router,
    dependencies=[Depends(get_current_active_user)]
)
api_router.include_router(
    services_router,
    dependencies=[Depends(get_current_active_user)]
)

# --- RUTAS PARA GESTIÓN OPERATIVA (EMPLOYEE Y ADMIN) ---
api_router.include_router(
    clients_router,
    dependencies=[Depends(get_current_active_user)]
)
api_router.include_router(
    vehicle_services,
    prefix="/operations",
    dependencies=[Depends(get_current_active_user)]
)
api_router.include_router(
    inventary_router,
    dependencies=[Depends(get_current_active_user)]
)
api_router.include_router(
    cashier_router,
    prefix="/cashier-ops",
    dependencies=[Depends(get_current_active_user)]
)

# --- RUTAS EXCLUSIVAS PARA ADMIN ---
# Nota: Se permite get_current_active_user en users_router para que el cliente acceda a /me
# El resto de métodos (list, delete) deben protegerse internamente en el router con get_current_admin
api_router.include_router(
    users_router,
    dependencies=[Depends(get_current_active_user)]
)
api_router.include_router(
    roles_router,
    dependencies=[Depends(get_current_admin)]
)
