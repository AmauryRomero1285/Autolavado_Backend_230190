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

# --- RUTAS PARA EMPLEADOS Y ADMIN ---
#services
api_router.include_router(
    services_router,
    dependencies=[Depends(get_current_active_user)]
)
#vehicles
api_router.include_router(
    vehicles_router,
    dependencies=[Depends(get_current_active_user)]
)
#clients
api_router.include_router(
    clients_router,
    dependencies=[Depends(get_current_active_user)]
)
#services
api_router.include_router(
    vehicle_services,
    dependencies=[Depends(get_current_active_user)]
)
#products
api_router.include_router(
    products_router,
    dependencies=[Depends(get_current_active_user)]
)
#invetary-movements
api_router.include_router(
    inventary_router,
    dependencies=[Depends(get_current_active_user)]
)
#cashier
api_router.include_router(
    cashier_router,
    dependencies=[Depends(get_current_active_user)]
)

# --- RUTAS EXCLUSIVAS PARA ADMIN ---
api_router.include_router(
    users_router,
    prefix="/users",
    dependencies=[Depends(get_current_admin)]
)
api_router.include_router(
    roles_router,
    prefix="/roles",
    dependencies=[Depends(get_current_admin)]
)

# --- RUTAS EXCLUSIVAS PARA CLIENTES
api_router.include_router(
    vehicles_router,
    prefix="/vehicles",
    dependencies=[Depends(get_current_client)]
)
