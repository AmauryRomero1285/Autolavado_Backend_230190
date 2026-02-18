@echo off
cd Autolavado_Backend_230190

:: Entrar a app y asegurar que existe schemas
cd app
if not exist schemas (
    mkdir schemas
)

:: Entrar a schemas para crear los archivos
cd schemas

:: Crear los archivos faltantes basados en la imagen
echo .> client_schema.py
echo .> services_schema.py
echo .> vehicle_services_schema.py
echo .> vehicle_schema.py
echo .> role_schema.py
echo .> user_schema.py

echo Estructura de Schemas actualizada con exito.
pause
