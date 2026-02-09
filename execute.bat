@echo off
cd Autolavado_Backend_230190
:: Crear estructura principal
mkdir app test docs
:: Crear subdirectorios en app
mkdir app\api\v1 app\models app\schemas app\services app\database app\core
:: crear archivos iniciales
echo .> app\__init__.py
echo .> app\main.py
echo .> app\api\v1\__init__.py
echo .> app\api\v1\clients.py
echo .> app\api\v1\employees.py
echo .> app\api\v1\cashiers.py
echo .> app\api\v1\vehicles.py
echo .> app\models\vehicle.py
echo .> requeriments.txt
echo .> env.example

echo Estructura de proyecto creada con exito.
pause