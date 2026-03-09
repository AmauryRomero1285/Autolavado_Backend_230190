# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn, MySQLDsn, validator
from typing import Optional, Literal


class Settings(BaseSettings):
    """
    Configuración centralizada de la aplicación.
    Los valores se leen preferentemente de variables de entorno (.env)
    """

    # ───────────────────────────────────────────────
    # General
    # ───────────────────────────────────────────────
    PROJECT_NAME: str = "Autolavado API"
    PROJECT_DESCRIPTION: str = "API RESTful para gestión de servicios de autolavado"
    VERSION: str = "1.0.0"

    API_V1_STR: str = "/api/v1"

    # Entorno: development | testing | production
    ENVIRONMENT: Literal["development", "testing", "production"] = "development"

    # ───────────────────────────────────────────────
    # Seguridad - JWT
    # ───────────────────────────────────────────────
    SECRET_KEY: str = Field(
        default="cambia-esto-por-un-secreto-muy-largo-y-seguro-128-caracteres-minimo",
        description="Clave secreta para firmar JWT. ¡Cambiar en producción!"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30   # tiempo de expiración del access token

    # ───────────────────────────────────────────────
    # Base de datos
    # ───────────────────────────────────────────────
    DATABASE_URL: str = Field(
        default="mysql+pymysql://root:1234@localhost:3306/autolavado_db",
        description="Cadena de conexión completa (preferiblemente en .env)"
    )

    # Opcional: si prefieres separar componentes (útil para migraciones alembic)
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_NAME: Optional[str] = None
    DB_DRIVER: str = "pymysql"  # o "aiomysql" si vas a usar async

    # Validación automática si usas componentes separados
    @validator("DATABASE_URL", pre=True, always=True)
    def build_database_url(cls, v, values):
        if v:
            return v
        # Construcción dinámica si se dan los componentes
        driver = values.get("DB_DRIVER", "pymysql")
        user = values.get("DB_USER", "root")
        password = values.get("DB_PASSWORD", "")
        host = values.get("DB_HOST", "localhost")
        port = values.get("DB_PORT", 3306)
        db_name = values.get("DB_NAME", "autolavado_db")
        return f"mysql+{driver}://{user}:{password}@{host}:{port}/{db_name}"

    # ───────────────────────────────────────────────
    # CORS (para frontend)
    # ───────────────────────────────────────────────
    BACKEND_CORS_ORIGINS: list[str] = ["*"]  # en producción: ["https://tudominio.com"]

    # ───────────────────────────────────────────────
    # Logging y debug
    # ───────────────────────────────────────────────
    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",              # lee automáticamente .env
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"                # ignora variables no definidas aquí
    )


# Instancia global (se importa donde sea necesario)
settings = Settings()