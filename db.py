from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Corregido: mysql+pymysql para que SQLAlchemy sepa qué driver usar
# 2. Asegúrate que la DB "autolavadoDB" ya esté creada en tu MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@127.0.0.1:3306/autolavadoDB"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True  # Recomendado para MySQL para evitar desconexiones inactivas
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Función útil para obtener la sesión en tus rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
