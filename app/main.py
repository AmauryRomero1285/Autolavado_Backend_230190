from fastapi import FastAPI
from app.api.v1.main import api_router

app = FastAPI(title="Autolavado API", version="1.0.0")

# Ruta de bienvenida
@app.get("/")
def home():
    return {"message": "Bienvenido a la API de Autolavado", "docs": "/docs"}

app.include_router(api_router)
