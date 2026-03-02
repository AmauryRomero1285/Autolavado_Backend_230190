from fastapi import FastAPI
from app.api.v1.main import api_router

app = FastAPI(title="Autolavado API", version="1.0.0")

app.include_router(api_router)