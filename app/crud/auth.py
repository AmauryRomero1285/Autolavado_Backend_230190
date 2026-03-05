# app/crud/auth.py
from sqlalchemy.orm import Session
from app.models.auth import UserSession

def create_session(db: Session, user_id: int, token: str):
    """Crea una nueva sesión y desactiva las anteriores del mismo usuario."""
    db.query(UserSession).filter(UserSession.user_id == user_id).update({"is_active": False})
    
    db_session = UserSession(user_id=user_id, token=token, is_active=True)
    db.add(db_session)
    db.commit()
    return db_session

def deactivate_session(db: Session, token: str):
    """Llamada desde el logout."""
    db.query(UserSession).filter(UserSession.token == token).update({"is_active": False})
    db.commit()

def get_session_by_token(db: Session, token: str):
    """
    Esta es la función que te pide deps.py. 
    Busca la sesión y devuelve el registro completo.
    """
    return db.query(UserSession).filter(
        UserSession.token == token, 
        UserSession.is_active == True
    ).first()
