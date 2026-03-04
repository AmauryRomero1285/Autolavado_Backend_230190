# models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)
    
    username = Column(String(60), nullable=False, unique=True, index=True)
    email = Column(String(120), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)     
    first_name = Column(String(60), nullable=True)
    last_name = Column(String(60), nullable=True)
    second_last_name = Column(String(60), nullable=True)
    phone_number = Column(String(20), nullable=True, index=True)
    address = Column(String(255), nullable=True)
    
    is_active = Column(Boolean, nullable=False, server_default="true", default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Relación útil para consultas ORM
    #role = relationship("Role", back_populates="users", lazy="selectin")