# pylint: disable=import-error, too-few-public-methods
'''
User Model Module.
Defines the structure for the tbb_users table.
'''
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from database.db import Base

class User(Base):
    '''
    Represents a user model in the database.
    '''
    __tablename__ = "tbb_users"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("tbc_role.id"))
    first_name = Column(String(60))
    last_name = Column(String(60))
    second_last_name = Column(String(60))
    username = Column(String(60))
    password = Column(String(60))
    address= Column(String(120))
    phone_number = Column(String(10))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
