from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm 
from typing import Annotated, Optional

from app import crud, models, schemas
from app.api.v1.deps import DBSession, oauth2_scheme, get_current_active_user_optional
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

# app/api/v1/auth.py

@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register(
    user_in: schemas.UserCreate, 
    db: DBSession,
    current_user: Annotated[Optional[models.User], Depends(get_current_active_user_optional)] = None 
):
    # 1. Verificar si el email ya existe
    if crud.user.get_user_by_email(db, email=user_in.email):
        raise HTTPException(status_code=400, detail="Este correo ya está registrado.")

    # 2. Lógica de ROL (ID 3 = User/Cliente por defecto)
    DEFAULT_ROLE_ID = 3
    final_role_id = DEFAULT_ROLE_ID

    # 3. Verificación de "Primer Administrador" en el sistema
    # Buscamos si existe al menos un usuario con rol admin (asumiendo ID 1 para Admin)
    admin_exists = db.query(models.User).join(models.Role).filter(
        models.Role.name.ilike("admin")
    ).first()

    # 4. Lógica de asignación de Roles
    if not admin_exists:
        # SI NO HAY ADMINS: Permitimos que el primer registro use el role_id que envíe 
        # (Ideal para el setup inicial del sistema)
        final_role_id = user_in.role_id or 1  # Si no envía, asume 1 (Admin)
    
    elif user_in.role_id and user_in.role_id != DEFAULT_ROLE_ID:
        # SI YA HAY ADMINS: Solo un Admin logueado puede asignar roles distintos al default
        is_admin = (
            current_user and 
            current_user.role and 
            current_user.role.name.lower() in ["admin", "administrador"]
        )
        
        if not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para asignar roles especiales."
            )
        
        # Si es Admin autenticado, aceptamos el ID enviado
        final_role_id = user_in.role_id

    # 5. Crear el usuario con la FK role_id validada
    return crud.user.create_user(db, user_in=user_in, role_id=final_role_id)




@router.post("/login", response_model=schemas.Token)
def login(
    db: DBSession,
    # Cambiamos UserLogin por OAuth2PasswordRequestForm para que funcione el botón de Swagger
    form_data: OAuth2PasswordRequestForm = Depends() 
):
    """Login compatible con Swagger y persistencia de sesión"""
    # Swagger envía el email/teléfono en form_data.username
    user = crud.user.get_user_by_email(db, email=form_data.username)
    
    if not user:
        # Intento por teléfono si el username es numérico
        if form_data.username.replace("+", "").isdigit():
            user = crud.user.get_by_phone(db, phone=form_data.username)

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    # --- Registrar la sesión en la base de datos ---
    crud.auth.create_session(db, user_id=user.id, token=access_token)
    
    return schemas.Token(access_token=access_token, token_type="bearer")

@router.post("/logout")
def logout(db: DBSession, token: str = Depends(oauth2_scheme)):
    """Invalida el token en la tabla user_sessions"""
    # Cambiamos el booleano is_active a False en la DB
    success = crud.auth.deactivate_session(db, token=token)
    if not success:
        raise HTTPException(status_code=404, detail="Token no encontrado o ya invalidado")
    
    return {"message": "Sesión cerrada exitosamente"}
