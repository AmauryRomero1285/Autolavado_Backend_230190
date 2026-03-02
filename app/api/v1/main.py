# app/api/v1/main.py
from fastapi import APIRouter

from .auth import router as auth_router
from .roles import router as roles_router
from .users import router as users_router
from .clients import router as clients_router
from .vehicles import router as vehicles_router
from .services import router as services_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(roles_router)
api_router.include_router(users_router)
api_router.include_router(clients_router)
api_router.include_router(vehicles_router)
api_router.include_router(services_router)