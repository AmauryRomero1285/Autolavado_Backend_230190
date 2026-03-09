from db import SessionLocal
from app.models.user import User

print("Modelos importados OK")

try:
    db = SessionLocal()
    print("Conexión abierta OK")
    db.query(User).limit(1).all()
    print("Consulta mínima OK")
    db.close()
except Exception as e:
    print("Error:", str(e))